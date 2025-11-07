import reflex as rx

def simple_icon(
    name: str, size: str = "24px", color: str | None = None
) -> rx.Component:
    name = name.lower()
    base_url = f"https://cdn.simpleicons.org/{name}"

    # 如果提供了颜色，直接使用
    if color is not None:
        url = f"{base_url}/{color.lstrip('#')}"
    else:
        color_var = rx.color_mode_cond(light="000", dark="fff")
        url = base_url + "/" + color_var

    return rx.image(src=url, width=size, height=size, alt=name)
