# calhacks11.py
import os
import reflex as rx
#from calhacks11.frontend.state import State
from backend import main
from openai import OpenAI
from pydantic import Field
import time
import asyncio


from rxconfig import config

class TimerState(rx.State):
    count: int = 0

    async def tick(self):
        await asyncio.sleep(1)
        self.count += 1
        global stopwatch
        stopwatch = self.count
        FormInputState.handle_submit()
        return TimerState.tick

class FormInputState(rx.State):
    assistant_id: str = ''
    conversation_id: str = ''
    response: str = ''
    summary: str = ''
    suggestions: str = ''
    watch_display: str = ''
    


    def init_assistant_and_conversation(self):
        if not self.assistant_id:
            assistant = main.createAssistant()
            self.assistant_id = assistant.id
        if not self.conversation_id:
            conversation = main.openConversation()
            self.conversation_id = conversation.id

    def handle_submit(self, form_data: dict):
        self.init_assistant_and_conversation()
        # Get the response as a dictionary
        global stopwatch
        try:
            stopwatch
        except NameError:
            stopwatch = 0
        response = main.handleConversation(self.conversation_id, self.assistant_id, form_data['input'], stopwatch)
        # Update the state variables
        self.summary = response.get('summary', '')
        self.suggestions = response.get('suggestions', '')
        self.response = response.get('full_response', '')


    
    # Function to create the assistant
def createAssistant():
    assistant = OpenAI.client.beta.assistants.create(
        name="Mental Health Assistant", 
        instructions="You are an assistant who is generating prompts to help a professional in talking to someone with mental health concerns. Generate potential responses for what the professional could say/ask", 
        tools=[{"type": "file_search"}],
        model="gpt-4"
    )
    return assistant  # This will have an 'id' attribute

# Function to open a new conversation thread
def openConversation():
    thread = OpenAI.client.beta.threads.create()
    return thread  # This will have an 'id' attribute



    @rx.var
    def response(self) -> str:
        return self.form_data.get('response', '')



    
def index() -> rx.Component:
    global start_time
    start_time = time.time()
    return rx.container(
        rx.flex(
            # Left column: Summary, Suggestions
            rx.vstack(
                rx.box(
                    rx.heading("Summary", size="lg", style={"text_decoration": "underline"}),
                    rx.text(
                        FormInputState.summary,
                        font_size="md",
                        padding="10px",
                    ),
                    padding="20px",
                    border="2px solid #000",
                    border_radius="10px",
                    box_shadow="lg",
                    margin="10px 0",
                    width="100%",
                    background_color="#b19e9a",
                    color="#000000",
                ),
                rx.box(
                    rx.heading("Suggestions", size="lg", style={"text_decoration": "underline"}),
                    rx.markdown(
                        FormInputState.suggestions,  # Directly use markdown format
                        font_size="md",
                        padding="10px",
                    ),
                    padding="20px",
                    border="2px solid #000",
                    border_radius="10px",
                    box_shadow="lg",
                    margin="10px 0",
                    width="100%",
                    background_color="#b19e9a",
                    color="#000000",
                ),

                rx.vstack(
                    rx.text(TimerState.count,
                    )
                    
                ),
                
                # TODO: REMOVE
                rx.box(
                    main.currTranscription('backend/Operator.mp3', 'backend/Caller.mp3', 100)
                ),
                spacing="20px",
                width="65%",
                align_items="stretch",
            ),
            # Right column: Chatbot
            rx.card(
                rx.vstack(
                    rx.heading("Chat"),
                    rx.form.root(
                        rx.hstack(
                            rx.input(
                                name='input',
                                placeholder='Prompt',
                                type='text',
                                required=True,
                            ),
                            rx.button('Submit', type='submit'),
                            position='relative',
                        ),
                        on_submit=FormInputState.handle_submit,
                        reset_on_submit=True
                    ),
                    rx.divider(),
                    rx.text(
                        FormInputState.response,
                        padding="10px",
                        style={"white_space": "pre-wrap"},  # Preserve line breaks
                    ),
                ),
                width="30%",
                padding="20px",
                border_radius="10px",
                box_shadow="lg",
                background_color="#A9A9A9",
            ),
            direction="row",
            width="100%",
            justify_content="space-between",
            align_items="flex-start",
            gap="20px",
        ),
        width="100%",
        margin="auto",
        padding="20px",
    )




style = {
    rx.text: {
        "font_family": "Comic Sans MS",
    },
    rx.box: {
        "font_family": "Comic Sans MS",
        "box_sizing": "border-box",
    },
    rx.input: {
        "font_family": "Comic Sans MS",
        "padding": "10px",
        "border_radius": "5px",
        "border": "1px solid #ccc",
    },
    rx.button: {
        "font_family": "Comic Sans MS",
        "padding": "10px 20px",
        "border_radius": "5px",
        "background_color": "#4CAF50",
        "color": "#000000",
        "border": "none",
        "cursor": "pointer",
    },
}






app = rx.App(
    #state=State,
    style=style,
)

app.add_page(index, on_load = TimerState.tick)


