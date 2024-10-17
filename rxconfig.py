import reflex as rx
import os

config = rx.Config(
    app_name="inventorymanagement",
    db_url=os.environ.get("DB_URL")
    )
