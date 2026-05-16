from typing import List, Optional
from pydantic import BaseModel, field_validator


class SupplierCreate(BaseModel):
    supplier_name: str
    contact_number: str
    city: str
    categories_supplied: List[str] = []
    active: bool = True

    @field_validator("supplier_name", "city")
    @classmethod
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip().title()

    model_config = {
        "json_schema_extra": {
            "example": {
                "supplier_name": "Raj Electronics",
                "contact_number": "+91-9876543210",
                "city": "Chennai",
                "categories_supplied": ["Electronics", "Cables"],
                "active": True
            }
        }
    }


class SupplierUpdate(BaseModel):
    supplier_name: Optional[str] = None
    contact_number: Optional[str] = None
    city: Optional[str] = None
    categories_supplied: Optional[List[str]] = None
    active: Optional[bool] = None
