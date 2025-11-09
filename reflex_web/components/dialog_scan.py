import re
import reflex as rx
from util.scan import scan

class DialogScan(rx.ComponentState):
    host: str = ""
    scan_links: list[dict[str, str | int]] = [{ "port": 12 }]
    loading: bool = False

    @staticmethod
    def format_host(value: str) -> str:
        if not value.startswith("http"):
            value = f"http://{value}"
        if value.endswith("/"):
            value = value[:-1]
        return value

    def on_host_change(self, value: str):
        self.host = value

    def on_host_blur(self, value: str):
        if value == "":
            return
        self.host = DialogScan.format_host(value)

    def on_open_change(self, open: bool):
        if not open:
            self.host = ""
            self.scan_links = [{ "port": 12 }]

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

    def on_confirm(self):
        print(self.scan_links)
        print(f"Confirming {self.host}")

    def on_port_change(self, value: str):
        self.scan_links[0]["port"] = int(value)

    @classmethod
    def get_component(cls, trigger: rx.Component) -> rx.Component:
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
                                    value=cls.host,
                                    placeholder="Enter your host",
                                    on_change=cls.on_host_change,
                                    on_blur=cls.on_host_blur
                                ),
                                rx.cond(
                                    cls.loading,
                                    rx.spinner(),
                                    rx.button(
                                        rx.icon("radar", size=18),
                                        size="1",
                                        variant="ghost",
                                        on_click=cls.on_scan
                                    )
                                ),
                                spacing="4",
                                align_items="center",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Port"),
                            rx.input(value=cls.scan_links[0]["port"], on_change=cls.on_port_change),
                            rx.foreach(
                                cls.scan_links,
                                lambda link, i: rx.flex(
                                    rx.text(link.port),
                                    rx.text(link.name),
                                    rx.text(link.url),
                                    spacing="2"
                                )
                            ),
                        ),
                        spacing="4",
                    ),
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button("Cancel", color_scheme="gray", variant="soft"),
                    ),
                    rx.button("Confirm", disabled=cls.loading, on_click=cls.on_confirm),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
            ),
            on_open_change=cls.on_open_change,
        )