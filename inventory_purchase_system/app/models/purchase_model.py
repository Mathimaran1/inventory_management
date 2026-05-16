from datetime import datetime, timezone
from beanie import Document
from pydantic import Field


class Purchase(Document):
    supplier_id: str
    item_id: str
    supplier_name: str
    item_name: str
    purchase_quantity: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "purchases"
