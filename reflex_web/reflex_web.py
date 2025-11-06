"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""
    count: int = 0

    def on_button_click(self):
        self.count += 1

@rx.page(route="/", title="Home")
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.switch(),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.text(f"Button clicked: {State.count} times", size="4"),
            rx.button(
                "Click me",
                on_click=State.on_button_click
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App(theme=rx.theme(appearance="dark"))
