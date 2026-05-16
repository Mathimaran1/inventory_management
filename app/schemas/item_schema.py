from typing import Optional
from pydantic import BaseModel, field_validator


class ItemCreate(BaseModel):
    item_name: str
    category: str
    price: float
    quantity: int = 0
    reorder_level: int = 10

    @field_validator("price")
    @classmethod
    def price_non_negative(cls, v):
        if v < 0:
            raise ValueError("Price cannot be negative")
        return round(v, 2)

    @field_validator("quantity", "reorder_level")
    @classmethod
    def non_negative(cls, v):
        if v < 0:
            raise ValueError("Value cannot be negative")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "item_name": "Wireless Mouse",
                "category": "Electronics",
                "price": 499.99,
                "quantity": 100,
                "reorder_level": 20
            }
        }
    }


class ItemUpdate(BaseModel):
    item_name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    reorder_level: Optional[int] = None


class StockReduce(BaseModel):
    reduce_by: int

    @field_validator("reduce_by")
    @classmethod
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("reduce_by must be greater than 0")
        return v

    model_config = {"json_schema_extra": {"example": {"reduce_by": 5}}}
