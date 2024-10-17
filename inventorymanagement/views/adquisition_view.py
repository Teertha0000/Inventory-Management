import reflex as rx
from reflex.components.radix.themes.base import LiteralAccentColor


def item(
    state: str, progress: int, color: LiteralAccentColor
) -> rx.Component:
    return rx.vstack(
        rx.text(
            state,
            size="2",
            weight="medium",
        ),
        rx.flex(
            rx.text(
                f"{progress}%",
                position="absolute",
                top="50%",
                left=["90%", "90%", "90%", "90%", "95%"],
                transform="translate(-50%, -50%)",
                size="2",
            ),
            rx.progress(
                value=progress,
                height="19px",
                color_scheme=color,
                width="100%",
            ),
            position="relative",
            width="100%",
        ),
        width="100%",
        align_items="flex-start",
        # spacing="1",
    )


def adquisition() -> rx.Component:
    return rx.vstack(
        item("Dhaka", 27, "blue"),
        item("Jessore", 25, "green"),
        item("Rangpur", 18, "orange"),
        item("Chittagong", 16, "crimson"),
        item("Khulna", 14, "plum"),
        width="100%",
        spacing="2",
    )
