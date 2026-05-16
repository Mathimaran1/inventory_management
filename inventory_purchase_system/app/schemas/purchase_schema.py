from pydantic import BaseModel, field_validator


class PurchaseCreate(BaseModel):
    supplier_id: str
    item_id: str
    purchase_quantity: int

    @field_validator("purchase_quantity")
    @classmethod
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("purchase_quantity must be greater than 0")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "supplier_id": "64f1a2b3c4d5e6f7a8b9c0d1",
                "item_id": "64f1a2b3c4d5e6f7a8b9c0d2",
                "purchase_quantity": 50
            }
        }
    }
