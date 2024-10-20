from openai import AsyncOpenAI
import reflex as rx


class State(rx.State):
    
    
    # curr question
    question: str = ""

    # chat history = list of (question, answer) tuples
    chat_history: list[tuple[str, str]] = []

    async def answer(self):
        client = AsyncOpenAI(
            api_key='YOUR_API_KEY'
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

        answer = ""
        self.chat_history.append((self.question, answer))

        self.question = ""
        yield

        async for item in session:
            if hasattr(item.choices[0].delta, "content"):
                if item.choices[0].delta.content is None:
                    break
                answer += item.choices[0].delta.content
                self.chat_history[-1] = (
                    self.chat_history[-1][0],
                    answer,
                )
                yield
