import reflex as rx
from typing import List
import pandas as pd
import io
from ..views import table_component
from sqlmodel import select
from collections import namedtuple
from .data import csv_data1


class Item(rx.Base):
    """The item class."""

    date: str
    wood_quantity: str
    chemical_quantity: str
    production_output: str
    production_revenue: str
    production_cost: str
    grade_a: str
    grade_b: str
    grade_c: str
    district: str
    volume: str
    id: str


class TableState(rx.State):
    """The state class."""
    items: List[Item] = []

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page
    entries: list["table_component.Table_data"] = []

    @rx.var(cache=True)
    def filtered_sorted_items(self) -> List[Item]:
        items = self.items

        # Filter items based on search value
        if self.search_value:
            search_value = self.search_value.lower()
            items = [
                item
                for item in items
                if any(
                    search_value in str(getattr(item, attr)).lower()
                    for attr in [
                        "date",
                        "wood_quantity",
                        "chemical_quantity",
                        "production_output",
                        "production_revenue",
                        "production_cost",
                        "grade_a",
                        "grade_b",
                        "grade_c",
                        "district",
                        "volume",
                        "id"
                    ]
                )
            ]

        return items

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 0
        )

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> list[Item]:
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_items[start_index:end_index]

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit

    def load_entries(self):
        with rx.session() as session:
            query = session.exec(select(table_component.Table_data)).all()
            self.entries = query
        # Sample data (add the rest of the data as needed)
        data_2 = self.entries

        # Start building CSV string
        csv_data = "date,wood_quantity,chemical_quantity,production_output,production_revenue,production_cost,grade_a,grade_b,grade_c,district,volume,id\n"

        # Append each row of data to the CSV string, matching the required structure
        for row in data_2:
            csv_data += f"{row.date},{row.wood_quantity},{row.chemical_quantity},{row.production_output},{row.production_revenue},{row.production_cost},{row.grade_a},{row.grade_b},{row.grade_c},{row.district},{row.volume},{row.id}\n"

        data = pd.read_csv(io.StringIO(csv_data))
        # Initialize the items list based on the DataFrame
        self.items = [Item(**row) for index, row in data.iterrows()]
        
        # Set the total_items to the number of items loaded
        self.total_items = len(self.items)

