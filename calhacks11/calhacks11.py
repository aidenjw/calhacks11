import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""
    ...


def index() -> rx.Component:
    return rx.container(
        rx.flex(
            rx.box(
                rx.heading("Summary"),
                rx.text("Lorem ipsum dolor sit amet, consectetur adipiscing elit."),
                padding='10px',
                border='1px solid black',
                flex=1,
            ),
            rx.box(
                rx.heading("Questions"),
                rx.text("Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."),
                padding='10px',
                border='1px solid black',
                flex=1,
            ),
            rx.box(
                rx.heading("Talking Suggestions"),
                rx.text("Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."),
                padding='10px',
                border='1px solid black',
                flex=1,
            ),
            direction='row',
            width='100%',
            justify_content='space-between',
        ),
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

app = rx.App(style=style)
app.add_page(index)
