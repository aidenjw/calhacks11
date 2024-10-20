import os
import reflex as rx
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
        return

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


    
            


    
    # Creating assistant
def createAssistant():
    assistant = OpenAI.client.beta.assistants.create(
        name="Mental Health Assistant", 
        instructions="You are an assistant who is generating prompts to help a professional in talking to someone with mental health concerns. Generate potential responses for what the professional could say/ask", 
        tools=[{"type": "file_search"}],
        model="gpt-4"
    )
    return assistant 


# Opening new conversation thread
def openConversation():
    thread = OpenAI.client.beta.threads.create()
    return thread 


# Widget handling
    
def index() -> rx.Component:
    global start_time
    start_time = time.time()
    return rx.container(
        rx.flex(
            
            # Left column: Summary and Suggestions
            rx.vstack(
                rx.box(
                    rx.heading("Crisis Companion", size="9", style={"text_decoration": "underline"}),
                    style={
                    "text_align": "center",},
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
                        FormInputState.suggestions, 
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
                            rx.button('Submit', type='submit', height = "20px"),
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
            style={"margin_top": "100px"},
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



# runtime app creation

app = rx.App(
    style=style,
)

app.add_page(index, on_load = TimerState.tick)


