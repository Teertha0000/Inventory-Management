import reflex as rx
import pandas as pd
from reflex.components.radix.themes.base import (
    LiteralAccentColor,
)
import csv
import io
from .table_component import Table_data
from sqlmodel import select
from typing import List
from .. import styles


class StatsState(rx.State):
    selected_tab: str = "volume"

    def set_selected_tab(self, tab: str):
        self.selected_tab = tab
    area_toggle: bool = True
    selected_tab: str = "volume"
    timeframe: str = "Monthly"
    volume_data = []
    production_data = []
    material_data = []
    device_data = []
    yearly_device_data = []
    entries: List["Table_data"] = []


    def toggle_areachart(self):
        self.area_toggle = not self.area_toggle
    def randomize_data(self):
        with rx.session() as session:
            query = session.exec(select(Table_data)).all()
            self.entries = query
        # Sample data (add the rest of the data as needed)
        data_2 = self.entries

        # Start building CSV string
        csv_data = "date,wood_quantity,chemical_quantity,production_output,production_revenue,production_cost,grade_a,grade_b,grade_c,district,volume\n"

        # Append each row of data to the CSV string, matching the required structure
        for row in data_2:
            csv_data += f"{row.date},{row.wood_quantity},{row.chemical_quantity},{row.production_output},{row.production_revenue},{row.production_cost},{row.grade_a},{row.grade_b},{row.grade_c},{row.district},{row.volume}\n"

        data = pd.read_csv(io.StringIO(csv_data))

        def production_data_from_csv():
            csvfile = pd.read_csv(io.StringIO(csv_data))
            data = []
            for row in csvfile.itertuples():
                month, day = row.date.split('-')
                data.append({'Date': f"{day}-{month}", 'Production': int(row.production_output)})

            return data
        
        production_data_1 = production_data_from_csv()

        # Example usage:
        self.production_data = production_data_1

        def material_data_from_csv():
            data = []
            csvfile = pd.read_csv(io.StringIO(csv_data))
            data = []
            for row in csvfile.itertuples():
                month, day = row.date.split('-')
                data.append({'Date': f"{day}-{month}", 'Woods': int(row.wood_quantity), 'Chemicals': int(row.chemical_quantity)})
            return data
        
        material_data_1 = material_data_from_csv()

        # Example usage:
        self.material_data = material_data_1


        def volume_data_from_csv():
            csvfile = pd.read_csv(io.StringIO(csv_data))
            data = []
            for row in csvfile.itertuples():
                month, day = row.date.split('-')
                data.append({'Date': f"{day}-{month}", 'Volume': int(row.volume)})
            return data
        
        volume_data_1 = volume_data_from_csv()

        # Example usage:
        self.volume_data = volume_data_1


        def calculate_grade_percentages():
            # Calculate percentage for each grade separately
            a_grade_percentage = data['grade_a'].mean()
            b_grade_percentage = data['grade_b'].mean()
            c_grade_percentage = data['grade_c'].mean()
            return a_grade_percentage, b_grade_percentage, c_grade_percentage
        a_grade, b_grade, c_grade = calculate_grade_percentages()

        self.device_data = [
            {"name": "A Grade", "value": (int(a_grade)), "fill": "var(--red-8)"},
            {"name": "B Grade", "value": (int(b_grade)), "fill": "var(--green-8)"},
            {"name": "C Grade", "value": (int(c_grade)), "fill": "var(--blue-8)"},
        ]

        self.yearly_device_data = [
            {"name": "A Grade", "value": 34, "fill": "var(--red-8)"},
            {"name": "B Grade", "value": 27, "fill": "var(--green-8)"},
            {"name": "C Grade", "value": 13, "fill": "var(--blue-8)"},
        ]


def area_toggle() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.icon_button(
            rx.icon("area-chart"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=StatsState.toggle_areachart,
        ),
        rx.icon_button(
            rx.icon("bar-chart-3"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=StatsState.toggle_areachart,
        ),
    )


def _create_gradient(color: LiteralAccentColor, id: str) -> rx.Component:
    return (
        rx.el.svg.defs(
            rx.el.svg.linear_gradient(
                rx.el.svg.stop(
                    stop_color=rx.color(color, 7), offset="5%", stop_opacity=0.8
                ),
                rx.el.svg.stop(stop_color=rx.color(color, 7), offset="95%", stop_opacity=0),
                x1=0,
                x2=0,
                y1=0,
                y2=1,
                id=id,
            ),
        ),
    )


def _custom_tooltip(color: LiteralAccentColor) -> rx.Component:
    return (
        rx.recharts.graphing_tooltip(
            separator=" : ",
            content_style={
                "backgroundColor": rx.color("gray", 1),
                "borderRadius": "var(--radius-2)",
                "borderWidth": "1px",
                "borderColor": rx.color(color, 7),
                "padding": "0.5rem",
                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
            },
            is_animation_active=True,
        ),
    )


def volume_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("blue", "colorBlue"),
            _custom_tooltip("blue"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Volume",
                stroke=rx.color("blue", 9),
                fill="url(#colorBlue)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.legend(),
            data=StatsState.volume_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            _custom_tooltip("blue"),
            rx.recharts.bar(
                data_key="Volume",
                stroke=rx.color("blue", 9),
                fill=rx.color("blue", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.legend(),
            data=StatsState.volume_data,
            height=425,
        ),
    )


def production_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("green", "colorGreen"),
            _custom_tooltip("green"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Production",
                stroke=rx.color("green", 9),
                fill="url(#colorGreen)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(domain=[50, 150], hide=True),
            rx.recharts.legend(),
            data=StatsState.production_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            _custom_tooltip("green"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.bar(
                data_key="Production",
                data=StatsState.production_data,
                stroke=rx.color("green", 9),
                fill=rx.color("green", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.legend(),
            data=StatsState.production_data,
            height=425,
        ),
    )
    


def material_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("purple", "colorPurple"),
            _custom_tooltip("purple"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Woods",
                stroke=rx.color("purple", 9),
                fill="url(#colorPurple)",
                type_="monotone",
            ),
            rx.recharts.area(
                data_key="Chemicals",
                stroke=rx.color("indigo", 9),
                fill="url(#colorPurple)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.legend(),
            data=StatsState.material_data,
            height=425,
        ),
        
        rx.recharts.bar_chart(
            _custom_tooltip("purple"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.bar(
                data_key="Woods",
                stroke=rx.color("purple", 9),
                fill=rx.color("purple", 7),
            ),
            rx.recharts.bar(
                data_key="Chemicals",
                stroke=rx.color("indigo", 9),
                fill=rx.color("indigo", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.legend(),
            data=StatsState.material_data,
            height=425,
        ),
    )


def pie_chart() -> rx.Component:
    return rx.cond(
        StatsState.timeframe == "Yearly",
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=StatsState.yearly_device_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                padding_angle=1,
                inner_radius="70",
                outer_radius="100",
                label=True,
            ),
            rx.recharts.legend(),
            height=300,
        ),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=StatsState.device_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                padding_angle=1,
                inner_radius="70",
                outer_radius="100",
                label=True,
            ),
            rx.recharts.legend(),
            height=300,
        ),
    )


def timeframe_select() -> rx.Component:
    return rx.select(
        ["Monthly", "Yearly"],
        default_value="Monthly",
        value=StatsState.timeframe,
        variant="surface",
        on_change=StatsState.set_timeframe,
    )

# def wood_result():
#     # Assuming the column you're interested in is named 'values'
#     values = data['wood_quantity'].tolist()

#     # Calculate the differences
#     differences = []
#     for i in range(1, len(values)):
#         differences.append(values[i-1] - values[i])

#     # Calculate the average of the differences
#     average_subtraction = sum(differences) // len(differences)

#     last_wood_quantity = data['wood_quantity'].iloc[-1]

#     wood_produce_time = last_wood_quantity // average_subtraction
#     return int(wood_produce_time)
# wood_left = (f"Inventory can produce wood for {wood_result()} days.").replace(".0", "")

# def chemical_result():
#     # Assuming the column you're interested in is named 'values'
#     values = data['chemical_quantity'].tolist()

#     # Calculate the differences
#     differences = []
#     for i in range(1, len(values)):
#         differences.append(values[i-1] - values[i])

#     # Calculate the average of the differences
#     average_subtraction = sum(differences) // len(differences)

#     last_chemical_quantity = data['chemical_quantity'].iloc[-1]

#     chemical_produce_time = last_chemical_quantity // average_subtraction

#     return int(chemical_produce_time)
# chemical_left = (f"Inventory can produce chemicals for {chemical_result()} days.").replace(".0", "")

# def wood_order_result():
#     if int(wood_result()) > 5:
#         return f"We need to order wood in {wood_result() - 5} days."
#     else:
#         return "We need to order wood as soon as possible."
    
# def wood_budget():
#     if int(wood_result()) > 5:
#         return f"After {wood_result()} days to restock wood:"
#     else:
#         return "For 30 days of wood:"

# def chemical_order_result():
#     if int(chemical_result()) > 5:
#         return f"We need to order chemical in {chemical_result() - 5} days."
#     else:
#         return "We need to order chemical as soon as possible."
    
# def chemical_budget():
#     if int(chemical_result()) > 5:
#         return f"After {chemical_result()} days to restock chemical:"
#     else:
#         return "For 30 days of chemical:"
    

# def inventory_analytics_data() -> dict:
#     """Fetch and return the inventory analytics data."""
#     return {
#         "wood_left": wood_left,  # Fetch or calculate your data here
#         "chemical_left": chemical_left,
#         "wood_order_result": wood_order_result(),
#         "chemical_order_result": chemical_order_result(),
#         "wood_budget_date": wood_budget(),
#         "chemical_budget_date": chemical_budget(),
#     }



# def volume_analytics_data() -> dict:
#     """Fetch and return the volume analytics data."""
#     max_volume = data['volume'].max()
#     last_volume = data['volume'].iloc[-1]
#     volume_left = int(max_volume - last_volume)
#     if max_volume > last_volume:
#         volume_state = (f"Volume is {volume_left} BDT below the maximum volume.")
#     else:
#         volume_state = (f"Volume is maxed out at {max_volume} BDT.")
    
#     total_volume = data['volume'].sum()
#     average_volume = int(total_volume // len(data['volume']))
#     average_sales_revenue = int(data['sales_revenue'].sum() // len(data['sales_revenue']))
#     average_production_cost = int(data['production_cost'].sum() // len(data['production_cost']))
#     avrage_revenue = average_sales_revenue - average_production_cost

#     days_leter_volume_wood = int(wood_result() * avrage_revenue)
#     wood_restock_volume1 = average_volume + days_leter_volume_wood
#     wood_restock_volume = wood_restock_volume1 - 8965000

#     days_leter_volume_chemical = int(chemical_result() * avrage_revenue)
#     chemical_restock_volume1 = average_volume + days_leter_volume_chemical
#     chemical_restock_volume = int(chemical_restock_volume1 - 8965000) - 1329391

#     thirty_days_letter_volume = last_volume + ((30 * average_volume) - 8965000) - 1329391

#     return {
#         "%_below/above": volume_state,
#         "wood_restock": f"after restocking wood {wood_result()} days leter, volume will be {wood_restock_volume} BDT.",
#         "chemical_restock": f"after restocking chemical {chemical_result()} days leter, volume will be {chemical_restock_volume} BDT.",
#         "month_letter_volume": f"After 30 days, volume will be {thirty_days_letter_volume} BDT.",
#     }

# def others() -> dict:
#     average_production = int(data['production_output'].sum() // len(data['production_output']))
#     last_production = data['production_output'].iloc[-1]
#     production_left = int(average_production - last_production)
#     need_to_produce = int(average_production + production_left)

#     if last_production < average_production:
#         production_state = f"We need to produce {need_to_produce} pieces of board tomorrow."
#     else:
#         production_state = f"Production is going well at {last_production} pieces per day."

#     every_day_revenue = int(data['sales_revenue'].sum() // len(data['sales_revenue']) - data['production_cost'].sum() // len(data['production_cost']))

#     district_most = data['district'].value_counts().idxmax()

#     production_cost = int(data['production_cost'].sum() // len(data['production_cost']))

#     return {"production_data": production_state,
#             "revnue_per_unit_production": f"In average, every day we earn {every_day_revenue} BDT.",
#             "most_sold_district": f"Most of the board sold in {district_most}.",
#             "production_cost": f"Everyday about {production_cost} BDT we need for production."}