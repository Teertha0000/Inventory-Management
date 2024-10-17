"""The overview page of the app."""
import reflex as rx
from .. import styles
from ..templates import template
from ..views.stats_cards import volume_card, production_output_card, inventory_card
from ..views import stats_cards
from ..views.charts import (
    volume_chart,
    production_chart,
    material_chart,
    area_toggle,
    pie_chart,
    timeframe_select,
    StatsState,
)
from ..views.adquisition_view import adquisition
from ..components.notification import notification
from ..components.card import card
from .profile import ProfileState



def _time_data() -> rx.Component:
    return rx.hstack(
        rx.tooltip(
            rx.icon("info", size=20),
            content=f"Graphs are based on the stored data."),
        rx.text("Data", size="4", weight="medium"),
        align="center",
        spacing="2",
    )


def tab_content_header() -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.hstack(
                rx.vstack(
                    _time_data(),
                    area_toggle(),
                    width="100%",
                    direction="row"
                ),
                rx.flex(
                    rx.tablet_and_desktop(
                        rx.segmented_control.root(
                            rx.segmented_control.item("Volume", value="volume"),
                            rx.segmented_control.item("Production", value="production"),
                            rx.segmented_control.item("Material", value="material"),
                            default_value="volume",
                            on_change=StatsState.set_selected_tab,
                        ),
                    ),
                    rx.mobile_only(
                        rx.select.root(
                            rx.select.trigger(placeholder="Volume"),
                            rx.select.content(
                                rx.select.item("Volume", value="volume"),
                                rx.select.item("Production", value="production"),
                                rx.select.item("Material", value="material"),
                            ),
                            on_change=StatsState.set_selected_tab,
                            default_value="volume",
                        ),
                    ),
                    width="auto",
                ),
                width="100%",
                justify="space-between",
            ),
            width="100%",
        ),
        rx.match(
            StatsState.selected_tab,
            ("volume", volume_chart()),
            ("production", production_chart()),
            ("material", material_chart()),
        ),
        width="100%",
    )


@template(route="/", title="Overview", on_load=[ StatsState.randomize_data, stats_cards.StatsState.load_entries, stats_cards.StatsState.calculate_the_num, stats_cards.StatsState.round_number, stats_cards.StatsState.calculate_the_num_p, stats_cards.StatsState.round_number_p])
def index() -> rx.Component:
    """The overview page.

    Returns:
        The UI for the overview page.
    """
    return rx.vstack(
        rx.heading(f"Welcome, {ProfileState.profile.name}", size="5"),
        rx.flex(
            rx.input(
                rx.input.slot(rx.icon("search"), padding_left="0"),
                placeholder="Search here...",
                size="3",
                width="100%",
                max_width="450px",
                radius="large",
                style=styles.ghost_input_style,
            ),
            rx.flex(
                notification("bell", "cyan", 12),
                notification("message-square-text", "plum", 6),
                spacing="4",
                width="100%",
                wrap="nowrap",
                justify="end",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        rx.grid(
            volume_card(),
            production_output_card(),
            inventory_card(),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(1, 1fr)",
                "repeat(2, 1fr)",
                "repeat(3, 1fr)",
                "repeat(3, 1fr)",
            ],
            width="100%"
            ),
        rx.card(tab_content_header(), width = "100%", box_shadow=styles.box_shadow_style),
        rx.grid(
    card(
        rx.hstack(
            rx.hstack(
                rx.icon("box", size=20),
                rx.text("Avarage Board Grade", size="5", weight="bold"),
                align="center",
                spacing="2",
            ),
            timeframe_select(),
            align="center",
            width="100%",
            justify="between",
        ),
        pie_chart(),
    ),
    card(
        rx.hstack(
            rx.icon("globe", size=20),
            rx.text("Sales Location", size="5", weight="bold"),
            align="center",
            spacing="2",
            margin_bottom="2.5em",
        ),
        rx.vstack(
            adquisition(),
        ),
    ),
    gap="1rem",
    grid_template_columns=[
        "1fr",
        "repeat(1, 1fr)",
        "repeat(2, 1fr)",
        "repeat(2, 1fr)",
        "repeat(2, 1fr)",
    ],
    width="100%",
),
        spacing="2rem",
        width="100%",
    )
