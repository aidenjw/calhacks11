import os
from openai import AsyncOpenAI
import reflex as rx
import asyncio


class State(rx.State):
    

    
    # The current question being asked.
    question: str = ""

    # Keep track of the chat history as a list of (question, answer) tuples.
    chat_history: list[tuple[str, str]] = []

    async def answer(self):
        # Our chatbot has some brains now!
        client = AsyncOpenAI(
            api_key='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'
        )

        session = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": self.question}
            ],
            stop=None,
            temperature=0.7,
            stream=True,
        )

        # Add to the answer as the chatbot responds.
        answer = ""
        self.chat_history.append((self.question, answer))

        # Clear the question input.
        self.question = ""
        # Yield here to clear the frontend input before continuing.
        yield

        async for item in session:
            if hasattr(item.choices[0].delta, "content"):
                if item.choices[0].delta.content is None:
                    # presence of 'None' indicates the end of the response
                    break
                answer += item.choices[0].delta.content
                self.chat_history[-1] = (
                    self.chat_history[-1][0],
                    answer,
                )
                yield
