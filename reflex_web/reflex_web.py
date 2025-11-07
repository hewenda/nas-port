import reflex as rx
from .views.home import index as home_index

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        radius="small",
        panel_background="translucent",
        scaling="90%",
        accent_color="sky",
        gray_color="sage"
    )
)

app.add_page(home_index, route="/")
