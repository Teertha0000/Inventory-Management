import reflex as rx
import os

config = rx.Config(
    app_name="inventorymanagement",
    db_url=os.environ.get("DB_URL", "postgresql://Inventory_Management_owner:S3fTU8YHzFko@ep-dawn-snow-a1o89k9i-pooler.ap-southeast-1.aws.neon.tech/Inventory_Management?sslmode=require")
    )
