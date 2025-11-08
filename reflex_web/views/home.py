import reflex as rx
from util.config import get_config
from reflex_web.layout import page_layout
from reflex_web.components.si_icon import simple_icon
from reflex_web.components.scan_modal import scan_modal

app_config = get_config()


class State(rx.State):
    searchText: str = ""

    @rx.event
    def on_search_change(self, value: str):
        self.searchText = value


def index() -> rx.Component:
    hosts = app_config["hosts"]
    host_components = []

    for host in hosts:
        links = host.get("links")
        host_name = host.get("host")
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
                    variant="classic",
                    as_child=True,
                )
            )
        host_components.append(
            rx.vstack(
                rx.heading(host_name, size="3"),
                rx.divider(size="4"),
                rx.grid(
                    links_components,
                    columns="3",
                    spacing="4",
                ),
                spacing="2",
            ),
        )

    content = rx.container(
        rx.stack(
            scan_modal(None, None),
            rx.vstack(host_components, spacing="4"),
            spacing="5",
            justify="center",
        ),
    )
    return page_layout(content)
