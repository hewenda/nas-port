import re
import reflex as rx
from util.scan import scan

class State(rx.State):
    host: str = ""
    scan_links: list[dict[str, str | int]] = []
    loading: bool = False

    @staticmethod
    def format_host(value: str) -> str:
        if not value.startswith("http"):
            value = f"http://{value}"
        if value.endswith("/"):
            value = value[:-1]
        return value

    @rx.event
    def on_host_change(self, value: str):
        self.host = value

    @rx.event
    def on_host_blur(self, value: str):
        if value == "":
            return
        self.host = State.format_host(value)

    @rx.event
    def on_open_change(self, open: bool):
        if not open:
            self.host = ""
            self.scan_links = []

    @rx.event
    async def on_scan(self):
        if not self.host or self.loading:
            return

        self.loading = True
        yield
        try:
            host = re.sub(r'^https?://', '', self.host)
            host = re.sub(r'/$', '', host)
            open_ports = await scan(host)
            self.scan_links = [{"port": port, "name": "", "url": f"http://{host}:{port}", "icon": ""} for port in open_ports]
        except Exception as e:
            yield rx.toast.error(str(e))
        finally:
            self.loading = False
            yield

    @rx.event
    def on_url_change(self, index: int, value: str):
        if 0 <= index < len(self.scan_links):
            new_links = self.scan_links.copy()
            new_links[index] = {**new_links[index], "url": value}
            self.scan_links = new_links

    @rx.event
    def on_icon_change(self, index: int, value: str):
        if 0 <= index < len(self.scan_links):
            new_links = self.scan_links.copy()
            new_links[index] = {**new_links[index], "icon": value}
            self.scan_links = new_links

    @rx.event
    def on_name_change(self, index: int, value: str):
        if 0 <= index < len(self.scan_links):
            new_links = self.scan_links.copy()
            new_links[index] = {**new_links[index], "name": value}
            self.scan_links = new_links

    @rx.event
    def on_confirm(self):
        print(f"Confirming {self.host}")

@rx.memo
def scan_modal(trigger: rx.Component) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
                trigger,
        ),
        rx.dialog.content(
            rx.dialog.title(
                rx.stack(
                    rx.heading(
                        "Scan",
                        size="3"
                    ),
                    spacing="4",
                    align_items="center",
                ),
            ),
            rx.form.root(
                rx.vstack(
                    rx.form.field(
                        rx.form.label("Host"),
                        rx.stack(
                            rx.input(
                                value=State.host,
                                placeholder="Enter your host",
                                on_change=State.on_host_change,
                                on_blur=State.on_host_blur
                            ),
                            rx.cond(
                                State.loading,
                                rx.spinner(),
                                rx.button(
                                    rx.icon("radar", size=18),
                                    size="1",
                                    variant="ghost",
                                    on_click=State.on_scan
                                )
                            ),
                            spacing="4",
                            align_items="center",
                        ),
                    ),
                    rx.form.field(
                        rx.form.label("Port"),
                        rx.grid(
                            rx.foreach(
                                State.scan_links,
                                lambda item, index: rx.stack(
                                    rx.text(item["port"], size="2"),
                                    rx.input(
                                        value=item["icon"],
                                        class_name="w-1/6",
                                        placeholder="Icon",
                                        on_change=lambda value, idx=index: State.on_icon_change(idx, value)
                                    ),
                                    rx.input(
                                        value=item["name"],
                                        placeholder="Name",
                                        on_change=lambda value, idx=index: State.on_name_change(idx, value)
                                    ),
                                    rx.input(
                                        value=item["url"],
                                        class_name="flex-auto",
                                        placeholder="URL",
                                        on_change=lambda value, idx=index: State.on_url_change(idx, value)
                                    ),
                                    spacing="2",
                                    align_items="center",
                                )
                            ),
                            columns="1",
                            spacing="2",
                        ),
                    ),
                    spacing="4",
                ),
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
        on_open_change=State.on_open_change,
    )