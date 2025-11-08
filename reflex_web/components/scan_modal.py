import reflex as rx
from util.scan import scan

class State(rx.State):
    host: str = ""
    scan_results: list[dict] = []
    links: list[dict] = []
    loading: bool = False

    @rx.event
    def on_host_change(self, value: str):
        self.host = value

    @rx.event
    async def on_scan(self):
        self.loading = True
        yield

        try:
            self.scan_results = await scan(self.host)
        except Exception as e:
            yield rx.toast.error(str(e))
        finally:
            self.loading = False

    @rx.event
    def on_confirm(self):
        print(f"Confirming {self.host}")

def scan_modal(host: str | None = None, links: list[dict] | None = None) -> rx.Component:
    if host is not None:
        state.host = host
    if links is not None:
        state.links = links

    return  rx.dialog.root(
        rx.dialog.trigger(rx.button("Scan", size="2")),
        rx.dialog.content(
            rx.dialog.title(
                rx.stack(
                    rx.heading(
                        rx.cond(State.host != "", State.host, "Scan"),
                        size="3"
                    ),
                    rx.cond(
                        State.loading,
                        rx.spinner(loading=State.loading),
                        rx.button(
                            rx.icon("radar", size=16),
                            size="1",
                            variant="ghost",
                            on_click=State.on_scan
                        )
                    ),
                    spacing="4",
                    align_items="center",
                ),
            ),
            rx.form.root(
                rx.vstack(
                    rx.form.field(
                        rx.form.label("Host"),
                        rx.input(value=State.host, placeholder="Enter your host", on_change=State.on_host_change)
                    ),
                    rx.form.field(
                        rx.form.label("Port"),
                        rx.grid(
                            rx.foreach(
                                State.scan_results,
                                lambda port: rx.stack(
                                    rx.text(port.get("port"), size="2"),
                                    rx.text(port.get("name"), size="2"),
                                    rx.text(port.get("proto"), size="2"),
                                )
                            ),
                            columns="3",
                            spacing="2",
                        ),
                    ),
                    spacing="4",
                ),
                on_submit=State.on_confirm,
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancel", color_scheme="gray", variant="soft"),
                ),
                rx.button("Confirm", disabled=State.loading),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
        ),
    )