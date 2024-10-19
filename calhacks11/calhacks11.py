import reflex as rx
from rxconfig import config

import openai
import os


class State(rx.State):
    ...


def index() -> rx.Component:
    return rx.container(
        rx.flex(
            rx.box(
                rx.heading("Summary", size="lg", style={"text_decoration": "underline"}),
                rx.text(
                    "aiden wang aiden wang aiden wang aiden wang aiden wang aiden wang",
                    font_size="md",
                    padding="10px"
                ),
                padding="20px",
                border="2px solid #000",
                border_radius="10px",
                box_shadow="lg",
                margin="10px",
                width="33%", 
                background_color="#b19e9a",
            ),
            rx.box(
                rx.heading("Suggestions", size="lg", style={"text_decoration": "underline"}),
                rx.text(
                    "aiden wang aiden wang aiden wang aiden wang aiden wang aiden wang",
                    font_size="md",
                    padding="10px"
                ),
                padding="20px",
                border="2px solid #000",
                border_radius="10px",
                box_shadow="lg",
                margin="10px",
                width="33%",  
                background_color="#b19e9a",

            ),
            rx.box(
                rx.heading("Risk Evaluation", size="lg", style={"text_decoration": "underline"}),
                rx.text(
                    "aiden wang aiden wang aiden wang aiden wang aiden wang aiden wang",
                    font_size="md",
                    padding="10px"
                ),
                padding="20px",
                border="2px solid #000",
                border_radius="10px",
                box_shadow="lg",
                margin="10px",
                width="33%",
                background_color="#b19e9a",
 
            ),
            direction="row",
            width="100%",
            justify_content="space-between",
            padding="20px",
        ),
        max_width="1920px",  
        margin="auto",  
        padding="20px", 
    )


style = {
    rx.text: {
        "font_family": "Comic Sans MS",
    },
    rx.box: {
        "font_family": "Comic Sans MS",
        "display": "inline-block",
    },
}

app = rx.App(state=State, style=style)
app.add_page(index)
