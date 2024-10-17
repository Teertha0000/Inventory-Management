import reflex as rx
from typing import List
from sqlmodel import select
# from ..backend import table_state
from sqlalchemy import func


class Table_data(rx.Model, table=True):
    """The customer model."""

    date: str
    wood_quantity: str
    chemical_quantity: str
    production_output: str
    production_revenue: str
    production_cost: float
    grade_a: str
    grade_b: str
    grade_c: str
    district: str
    volume: str

class State(rx.State):
    """The app state."""
    users: List[Table_data] = []
    sort_value: str = ""
    sort_reverse: bool = False
    search_value: str = ""
    current_data: Table_data = Table_data()

    entries: List["Table_data"] = []

    # entries = rx.session

    def get_all_entries(self):
        """Get all entries from the database."""
        with rx.session() as session:
            query = session.exec(select(Table_data)).all()
            self.entries = query


    def add_data_to_db(self, form_data: dict):
        self.current_data = form_data
    
        with rx.session() as session:
            db_entries = Table_data(**form_data)
            session.add(db_entries)
            # Reload the entries
            session.commit()
        self.get_all_entries()
        return rx.toast.info(f"Date {self.current_data['date']} has been added.", position="bottom-right")
    
    
    def get_user(self, data: Table_data):
        self.current_data = data


    def update_data_to_db(self, form_data: dict):
        self.current_data.update(form_data)
        with rx.session() as session:
            customer = session.exec(
                select(Table_data).where(Table_data.date == self.current_data["date"])
            ).first()
            for field in Table_data.get_fields():
                if field != "id":
                    setattr(customer, field, self.current_data[field])
            session.add(customer)
            session.commit()
        return rx.toast.info(f"Date {self.current_data['date']} has been updated.", position="bottom-right")


    def delete_data(self, id: dict):
        """Delete a customer from the database if more than 2 records exist."""
        with rx.session() as session:
            # First, count the total number of records
            total_records = session.exec(select(func.count(Table_data.id))).one()
            
            if total_records > 2:
                customer = session.exec(select(Table_data).where(Table_data.date == id["date"])).first()
                if customer:
                    session.delete(customer)
                    session.commit()
                    return rx.toast.info(f"Date {customer.date} has been deleted.", position="bottom-right")
            else:
                return rx.toast.warning("Cannot delete. Minimum 2 records must be maintained.", position="bottom-right")
