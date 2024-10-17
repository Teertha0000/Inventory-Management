import reflex as rx
from .. import styles
import pandas as pd
import io
import reflex as rx
from ..views import table_component
from sqlmodel import select
from typing import List

def format_number(value):
    return value

def gretter(first, second):
    return first > second

def and_gretter(first, second, third, fourth):
    return first < second and third < fourth


# Function to create Volume Card
def volume_card() -> rx.Component:
    i_d = rx.cond(
            gretter(StatsState.last_row, StatsState.prev_row),
            "increase from last day",
            "decrease from last day",
        )
    col = rx.cond(
            gretter(StatsState.last_row, StatsState.prev_row),
            rx.color("grass", 9),
            rx.color("tomato", 9),
        )

    positive_percentage = StatsState.v_rounded_value

    ico = rx.cond(
            gretter(StatsState.last_row, StatsState.prev_row),
            rx.icon(tag="trending-up", size=24, color=col),
            rx.icon(tag="trending-down", size=24, color=col),
        )

    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="dollar-sign", size=34),
                    color_scheme="blue",
                    radius="full",
                    padding="0.7rem",
                ),
                rx.vstack(
                    rx.heading(f"${StatsState.last_row:,.3f}", size="6", weight="bold"),
                    rx.text("Volume", size="4", weight="medium"),
                    spacing="1",
                    height="100%",
                    align_items="start",
                    width="100%",
                ),
                height="100%",
                spacing="4",
                align="center",
                width="100%",
            ),
            rx.hstack(
                ico,
                rx.text(positive_percentage, size="3", color=col, weight="medium"),
                rx.text(i_d, size="2", color=rx.color("gray", 10)),
                spacing="2",
                align="center",
            ),
            spacing="3",
        ),
        size="3",
        width="100%",
        box_shadow=styles.box_shadow_style,
    )

# Function to create Production Output Card
def production_output_card() -> rx.Component:
    icon = "hammer"
    icon_color = "green"

    col = rx.cond(
            gretter(StatsState.production_last_row, StatsState.average_output),
            rx.color("grass", 9),
            rx.color("tomato", 9),
        )

    ico = rx.cond(
            gretter(StatsState.production_last_row, StatsState.average_output),
            rx.icon(tag="trending-up", size=24, color=col),
            rx.icon(tag="trending-down", size=24, color=col),
        )
    
    change = rx.cond(
            gretter(StatsState.production_last_row, StatsState.average_output),
            "above",
            "billow"
        )
    
    percentage_change = StatsState.rounded_value_p

    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon(tag=icon, size=34),
                    color_scheme=icon_color,
                    radius="full",
                    padding="0.7rem",
                ),
                rx.vstack(
                    rx.heading(f"{StatsState.production_last_row:,} pieces", size="6", weight="bold"),
                    rx.text("Production Output", size="4", weight="medium"),
                    spacing="1",
                    height="100%",
                    align_items="start",
                    width="100%",
                ),
                height="100%",
                spacing="4",
                align="center",
                width="100%",
            ),
            rx.hstack(
                ico,
                rx.text(f"{percentage_change}%", size="3", color=col, weight="medium"),
                rx.text(f"{change} than average", size="2", color=rx.color("gray", 10)),
                spacing="2",
                align="center",
            ),
            spacing="3",
        ),
        size="3",
        width="100%",
        box_shadow=styles.box_shadow_style,
    )

# Function to create Inventory Card
def inventory_card() -> rx.Component:
    icon = "boxes"
    icon_color = "purple"
    wood_data = f"Wood: {StatsState.last_wood_quantity}m³"
    chemical_data = f" Chemical: {StatsState.last_chemical_quantity} bbl"
    warning_messages = "we have enough material."

    value = rx.cond(
        gretter(80, StatsState.last_wood_quantity),
        "Wood is about to running out.",
        warning_messages)

    warning_messages = value

    value = rx.cond(
        gretter(25 , StatsState.last_chemical_quantity),
        "Chemical is about to running out.",
        warning_messages)

    warning_messages = value

    value = rx.cond(
        gretter(80, StatsState.last_wood_quantity) & gretter(25, StatsState.last_chemical_quantity),
        "Wood and chemical is about to running out.",
        warning_messages)

    warning_messages = value

    children = [
        rx.vstack(
            rx.hstack(
        rx.badge(
            rx.icon(tag=icon, size=34),
            color_scheme=icon_color,
            radius="full",
            padding="0.7rem",
        ),
        rx.vstack(
            rx.heading(wood_data, size="4", weight="bold"),
            rx.heading(chemical_data, size="4", weight="bold"),
            rx.text("Inventory", size="3", weight="medium"),
            spacing="1",
            height="100%",
            align_items="start",
            width="100%",
        ),))
    ]

    # Add warning message at the end if it exists
    children.append(
        rx.text(warning_messages),
    )

    return rx.card(
        rx.vstack(
            *children,
            spacing="3",
        ),
        size="3",
        width="100%",
        box_shadow=styles.box_shadow_style,
    )


class StatsState(rx.State):
    entries: List[table_component.Table_data] = []
    prev_row: float = 0
    last_row: float = 0
    production_last_row: float = 0
    average_output: float = 0
    last_wood_quantity: int = 0
    last_chemical_quantity: int = 0
    the_num: float = 0
    v_rounded_value: float = 0
    the_num_p: float = 0
    rounded_value_p: float = 0

    def calculate_the_num(self):
        self.the_num = (((self.prev_row - self.last_row) / self.prev_row) * 100)

    def round_number(self):
        return rx.call_script(
            f"Math.floor(Math.abs({self.the_num}))",
            callback=StatsState.set_rounded_value
        )

    def set_rounded_value(self, value):
        self.v_rounded_value = value



    def calculate_the_num_p(self):
        self.the_num_p = (((self.production_last_row - self.average_output) / self.average_output) * 100)

    def round_number_p(self):
        return rx.call_script(
            f"Math.floor(Math.abs({self.the_num_p}))",
            callback=StatsState.set_rounded_value_p
        )

    def set_rounded_value_p(self, value):
        self.rounded_value_p = value


    def load_entries(self):
        with rx.session() as session:
            self.entries = session.exec(select(table_component.Table_data)).all()
        
        # Sample data (add the rest of the data as needed)
        data_2 = self.entries

        # Start building CSV string
        csv_data = "date,wood_quantity,chemical_quantity,production_output,production_revenue,production_cost,grade_a,grade_b,grade_c,district,volume\n"

        # Append each row of data to the CSV string, matching the required structure
        for row in data_2:
            csv_data += f"{row.date},{row.wood_quantity},{row.chemical_quantity},{row.production_output},{row.production_revenue},{row.production_cost},{row.grade_a},{row.grade_b},{row.grade_c},{row.district},{row.volume}\n"

        data = pd.read_csv(io.StringIO(csv_data))
        self.prev_row = int(data['volume'].iloc[-2])
        self.last_row = int(data['volume'].iloc[-1])
        self.production_last_row = int(data['production_output'].iloc[-1])
        self.average_output = int(data['production_output'].mean())
        self.last_wood_quantity = int(data['wood_quantity'].iloc[-1])
        self.last_chemical_quantity = int(data['chemical_quantity'].iloc[-1])
