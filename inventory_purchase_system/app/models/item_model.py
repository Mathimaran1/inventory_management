from datetime import datetime, timezone
from beanie import Document
from pydantic import Field


class Item(Document):
    item_name: str
    category: str
    price: float
    quantity: int = 0
    reorder_level: int = 10
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "items"

    @property
    def is_low_stock(self) -> bool:
        return self.quantity <= self.reorder_level
