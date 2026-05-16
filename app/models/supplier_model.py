from datetime import datetime, timezone
from typing import List
from beanie import Document
from pydantic import Field


class Supplier(Document):
    supplier_name: str
    contact_number: str
    city: str
    categories_supplied: List[str] = []
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "suppliers"
