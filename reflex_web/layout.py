"""全局组件定义"""

import reflex as rx
from reflex.style import set_color_mode, color_mode
from reflex_web.components.dialog_scan import DialogScan


def navbar() -> rx.Component:
    dialog_scan = DialogScan.create(
        trigger=rx.button(rx.icon("circle-plus", size=14, cursor="pointer"), variant="ghost")
    )

    return rx.box(
        rx.desktop_only(
            rx.hstack(
                dialog_scan,
                toggle_color_mode(),
                justify="end",
                spacing="5",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.menu.root(
                rx.menu.trigger(rx.icon("menu", size=24)),
                rx.menu.content(toggle_color_mode()),
                justify="end",
            ),
        ),
        padding="1em",
        position="sticky",
        top="0px",
        z_index="5",
        width="100%",
    )


def toggle_color_mode() -> rx.Component:
    return rx.segmented_control.root(
        rx.segmented_control.item(
            rx.icon(tag="monitor", size=14),
            value="system",
        ),
        rx.segmented_control.item(
            rx.icon(tag="sun", size=14),
            value="light",
        ),
        rx.segmented_control.item(
            rx.icon(tag="moon", size=14),
            value="dark",
        ),
        on_change=set_color_mode,
        variant="surface",
        value=color_mode,
    )


def page_layout(content: rx.Component) -> rx.Component:
    """页面布局组件，包含全局 header 和内容"""
    return rx.fragment(
        navbar(),
        content,
    )
