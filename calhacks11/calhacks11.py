import os
import reflex as rx
from state import State

from rxconfig import config

class State(rx.State):
    pass
    

def index() -> rx.Component:
    return rx.container(
        # Existing content
        rx.flex(
            rx.box(
                rx.heading("Summary", size="lg", style={"text_decoration": "underline"}),
                rx.text(
                    "aiden wang aiden wang aiden wang aiden wang aiden wang aiden wang",
                    font_size="md",
                    padding="10px",
                ),
                padding="20px",
                border="2px solid #000",
                border_radius="10px",
                box_shadow="lg",
                margin="10px 0",
                flex="1",
                background_color="#b19e9a",
                color="#000000",
            ),
            rx.box(
                rx.heading("Suggestions", size="lg", style={"text_decoration": "underline"}),
                rx.text(
                    "aiden wang aiden wang aiden wang aiden wang aiden wang aiden wang",
                    font_size="md",
                    padding="10px",
                ),
                padding="20px",
                border="2px solid #000",
                border_radius="10px",
                box_shadow="lg",
                margin="10px 0",
                flex="1",
                background_color="#b19e9a",
                color="#000000",
            ),
            rx.box(
                rx.heading("Risk Evaluation", size="lg", style={"text_decoration": "underline"}),
                rx.text(
                    "aiden wang aiden wang aiden wang aiden wang aiden wang aiden wang",
                    font_size="md",
                    padding="10px",
                ),
                padding="20px",
                border="2px solid #000",
                border_radius="10px",
                box_shadow="lg",
                margin="10px 0",
                flex="1",
                background_color="#b19e9a",
                color="#000000",
            ),
            direction="row",
            width="100%",
            justify_content="space-between",
            gap="20px",
            flex_wrap="wrap",
        ),
        # text input
        rx.box(
            rx.heading("Prompt", size="lg", style={"text_decoration": "underline"}),
            rx.form(
                rx.flex(
                    rx.input(
                        name="user_question",
                        placeholder="Type your question here...",
                        width="100%",
                        height="50px",
                        id="user_question",
                    ),
                    rx.button(
                        "Send",
                        type="submit",
                        margin_left="10px",
                    ),
                    direction="row",
                    align_items="center",
                    width="100%",
                ),
                on_submit=State.handle_submit,
            ),
            padding="20px",
            border="2px solid #000",
            border_radius="10px",
            box_shadow="lg",
            margin="20px 0",
            background_color="#b19e9a",
            width="100%",
            color="#000000",
        ),
        rx.box(
            rx.heading("Stored Input", size="lg", style={"text_decoration": "underline"}),
            rx.text(
                State.user_question,
                font_size="md",
                padding="10px",
            ),
            padding="20px",
            border="2px solid #000",
            border_radius="10px",
            box_shadow="lg",
            margin="20px 0",
            background_color="#e0e0e0",
            width="100%",
            color="#000000",
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
    state=State,
    style=style,
)
app.add_page(index)
