import reflex as rx
from ..backend.table_state import TableState, Item
from .table_component import State
from datetime import datetime

    
def edit_form_field(
    label: str,
    placeholder: str,
    type: str,
    name: str,
    icon: str,
    default_value: str = "",
    disabled: bool = False
) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.hstack(
                rx.icon(icon, size=16, stroke_width=1.5),
                rx.form.label(label),
                align="center",
                spacing="2",
            ),
            rx.form.control(
                rx.input(
                    placeholder=placeholder, type=type, default_value=default_value, disabled=disabled, required=True
                ),
                as_child=True,
            ),
            direction="column",
            spacing="1",
        ),
        name=name,
        width="100%",
    )


def form_field(
    label: str,
    placeholder: str,
    type: str,
    name: str,
    icon: str,
    disabled: bool = False,
    default_value: str = "",  # Add default_value parameter
) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.hstack(
                rx.icon(icon, size=16, stroke_width=1.5),
                rx.form.label(label),
                align="center",
                spacing="2",
            ),
            rx.form.control(
                rx.input(
                    placeholder=placeholder, type=type, disabled=disabled, default_value=default_value, required=True  # Use default_value here
                ),
                as_child=True,
            ),
            direction="column",
            spacing="1",
        ),
        name=name,
        width="100%",
    )
def add_data_button() -> rx.Component:
    today_date = datetime.now().strftime("%m-%d")  # Format date as MM-DD for input
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add Data", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="file-text", size=34),
                    color_scheme="grass",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Add New Data",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Fill the form with the data",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        # Date
                        form_field("Date", "Today's date", "text", "date", "calendar", default_value=today_date),  # Set the date field as disabled
                        # Wood Quantity
                        form_field("Wood Quantity", "Quantity of wood", "number", "wood_quantity", "tree-pine"),
                        # Chemical Quantity
                        form_field("Chemical Quantity", "Quantity of chemical", "number", "chemical_quantity", "flask-conical"),
                        # Production Output
                        form_field("Production Output", "Output of the production", "text", "production_output", "hammer"),
                        # Production Revenue
                        form_field("Production Revenue", "Revenue from production", "number", "production_revenue", "dollar-sign"),
                        # Production Cost
                        form_field("Production Cost", "Cost of the production", "number", "production_cost", "dollar-sign"),
                        # Grade A
                        form_field("Grade A", "Boards produced with grade A", "number", "grade_a", "package"),
                        # Grade B
                        form_field("Grade B", "Boards produced with grade B", "number", "grade_b", "package"),
                        # Grade C
                        form_field("Grade C", "Boards produced with grade C", "number", "grade_c", "package"),
                        # District
                        form_field("District", "District where boards sold", "text", "district", "map-pin"),
                        # Volume
                        form_field("Volume", "Volume of that day", "text", "volume", "trending-up"),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button("Cancel", variant="soft", color_scheme="gray"),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Add Data"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=State.add_data_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )
def edit_data_button(user):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("square-pen", size=22),
                rx.text("Edit", size="3"),
                color_scheme="blue",
                size="2",
                variant="solid",
                on_click=lambda: State.get_user(user),
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="square-pen", size=34),
                    color_scheme="grass",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Edit Data",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Edit the stored data",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        # Date
                        edit_form_field("Date", "Date of the data", "text", "date", "calendar", user.date, True),
                        # Wood Quantity
                        edit_form_field("Wood Quantity", "Quantity of wood", "number", "wood_quantity", "tree-pine", user.wood_quantity),
                        # Chemical Quantity
                        edit_form_field("Chemical Quantity", "Quantity of chemical", "number", "chemical_quantity", "flask-conical", user.chemical_quantity),
                        # Production Output
                        edit_form_field("Production Output", "Output of the production", "text", "production_output", "hammer", user.production_output),
                        # Production Revenue
                        edit_form_field("Production Revenue", "Revenue from production", "number", "production_revenue", "dollar-sign", user.production_revenue),
                        # Production Cost
                        edit_form_field("Production Cost", "Cost of the production", "number", "production_cost", "dollar-sign", user.production_cost),
                        # Grade A
                        edit_form_field("Grade A", "Boards produced with grade A", "number", "grade_a", "package", user.grade_a),
                        # Grade B
                        edit_form_field("Grade B", "Boards produced with grade B", "number", "grade_b", "package", user.grade_b),
                        # Grade C
                        edit_form_field("Grade C", "Boards produced with grade C", "number", "grade_c", "package", user.grade_c),
                        # District
                        edit_form_field("District", "District where boards sold", "text", "district", "map-pin", user.district),
                        # Volume
                        edit_form_field("Volume", "Volume of that day", "text", "volume", "trending-up", user.volume),
                        direction="column",
                        spacing="3",
                    ),
                     rx.flex(
                        rx.dialog.close(
                            rx.button("Cancel", variant="soft", color_scheme="gray"),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Update Data", type="submit")
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=State.update_data_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )
def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )
def _show_item(item: Item, index: int) -> rx.Component:
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),
    )
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),
    )
    return rx.table.row(
        rx.table.row_header_cell(item.date),
        rx.table.cell(item.wood_quantity),
        rx.table.cell(item.chemical_quantity),
        rx.table.cell(item.production_output),
        rx.table.cell(item.production_revenue),
        rx.table.cell(item.production_cost),
        rx.table.cell(item.grade_a),
        rx.table.cell(item.grade_b),
        rx.table.cell(item.grade_c),
        rx.table.cell(item.district),
        rx.table.cell(item.volume),
        rx.table.cell(item.id),
        rx.table.cell(rx.hstack(edit_data_button(item), 
                                rx.button(
                                        rx.icon("trash-2", size=22),
                                            size="2",
                                            variant="solid",
                                            color_scheme="red",
                                            on_click=State.delete_data(item))
                                            )),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )

def _pagination_view() -> rx.Component:
    return (
        rx.hstack(
            rx.text(
                "Page ",
                rx.code(TableState.page_number),
                f" of {TableState.total_pages}",
                justify="end",
            ),
            rx.hstack(
                rx.icon_button(
                    rx.icon("chevrons-left", size=18),
                    on_click=TableState.first_page,
                    opacity=rx.cond(TableState.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(TableState.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-left", size=18),
                    on_click=TableState.prev_page,
                    opacity=rx.cond(TableState.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(TableState.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-right", size=18),
                    on_click=TableState.next_page,
                    opacity=rx.cond(
                        TableState.page_number == TableState.total_pages, 0.6, 1
                    ),
                    color_scheme=rx.cond(
                        TableState.page_number == TableState.total_pages,
                        "gray",
                        "accent",
                    ),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevrons-right", size=18),
                    on_click=TableState.last_page,
                    opacity=rx.cond(
                        TableState.page_number == TableState.total_pages, 0.6, 1
                    ),
                    color_scheme=rx.cond(
                        TableState.page_number == TableState.total_pages,
                        "gray",
                        "accent",
                    ),
                    variant="soft",
                ),
                align="center",
                spacing="2",
                justify="end",
            ),
            spacing="5",
            margin_top="1em",
            align="center",
            width="100%",
            justify="end",
        ),
    )


def main_table() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.flex(
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    rx.input.slot(
                        rx.icon("x"),
                        justify="end",
                        cursor="pointer",
                        on_click=TableState.setvar("search_value", ""),
                        display=rx.cond(TableState.search_value, "flex", "none"),
                    ),
                    value=TableState.search_value,
                    placeholder="Search here...",
                    size="3",
                    max_width=["180px", "180px", "200px", "250px"],
                    width="100%",
                    variant="surface",
                    color_scheme="gray",
                    on_change=TableState.set_search_value,
                ),
                rx.spacer(spacing="1em"),
                add_data_button(),
                align="center",
                justify="end",
                spacing="3",
            ),
            rx.button(
                rx.icon("arrow-down-to-line", size=20),
                "Export",
                size="3",
                variant="surface",
                display=["none", "none", "none", "flex"],
                on_click=rx.download(url="/Data.csv"),
            ),
            spacing="3",
            justify="between",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("date", "calendar"),
                    _header_cell("wood quantity", "tree-pine"),
                    _header_cell("chemical quantity", "flask-conical"),
                    _header_cell("production output", "hammer"),
                    _header_cell("production revenue", "badge-dollar-sign"),
                    _header_cell("production cost", "badge-dollar-sign"),
                    _header_cell("grade a", "package"),
                    _header_cell("grade b", "package"),
                    _header_cell("grade c", "package"),
                    _header_cell("district", "map-pinned"),
                    _header_cell("volume", "trending-up"),
                    _header_cell("id", "key-round"),
                    _header_cell("actions", "cog"),
                    text_align="center",
                ),
            ),
            rx.table.body(
                rx.foreach(
                    TableState.get_current_page,
                    lambda item, index: _show_item(item, index),
                )
            ),
            variant="surface",
            size="3",
            width="100%",
            on_mount=State.get_all_entries,
        ),
        _pagination_view(),
        width="100%",
    )