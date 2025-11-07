import reflex as rx


def liquid_svg() -> rx.Component:
    return (
        rx.html(
            """
       <svg width='0' height='0' style='position:absolute;left:-9999px;top:-9999px'>
            <defs>
                <filter id='liquid_glass_filter'>
                <!-- 產生碎形雜訊 -->
                <feTurbulence type='fractalNoise' baseFrequency='0.003' numOctaves='2' seed='7' result='noise'/>
                <!-- 將雜訊模糊化，讓它更平滑 -->
                <feGaussianBlur in='noise' stdDeviation='1.2' result='map'/>
                <!-- 用模糊後的雜訊圖來扭曲我們的元素 -->
                <feDisplacementMap in='SourceGraphic' in2='map' scale='110' xChannelSelector='R' yChannelSelector='G'/>
                </filter>
            </defs>
            </svg>
            """
        ),
    )


liquid_style = {
    "backdrop-filter": "blur(4px) url(#liquid_glass_filter)",
    "box-shadow": (
        "inset 0 1px 0 rgba(255,255,255,0.45), "
        "inset 0 -1px 0 rgba(255,255,255,0.18), "
        "inset 6px 6px 16px rgba(255,255,255,0.12), "
        "0 10px 28px rgba(0,0,0,0.35)"
    ),
    "background": "rgba(255,255,255,0.1)",
}
