import reflex as rx
from util.config import get_config
from reflex_web.layout import page_layout
from reflex_web.components.si_icon import simple_icon

app_config = get_config()


class State(rx.State):
    searchText: str = ""

    @rx.event
    def on_search_change(self, value: str):
        self.searchText = value


def index() -> rx.Component:
    links = app_config["links"]
    links_components = []
    for link in links:
        port = link.get("port")
        icon = link.get("icon")
        name = link.get("name")
        url = link.get("url")

        links_components.append(
            rx.card(
                rx.link(
                    rx.flex(
                        simple_icon(name=icon),
                        rx.hstack(
                            rx.heading(name, size="4")
                            if name
                            else rx.icon("bone", size=14),
                            rx.text.quote(port, size="2") if port else None,
                            spacing="4",
                            flex="1",
                            align="baseline",
                        ),
                        spacing="4",
                        justify="between",
                        align_items="center",
                    ),
                    target="_blank",
                    href=url,
                    underline="none",
                ),
                size="2",
                as_child=True,
            )
        )

    content = rx.container(
        rx.stack(
            rx.grid(
                links_components,
                columns="3",
                spacing="4",
                width="100%",
            ),
            spacing="5",
            justify="center",
        ),
    )
    return page_layout(content)
