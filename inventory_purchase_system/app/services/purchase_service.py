from datetime import datetime, timezone

from beanie import PydanticObjectId
from fastapi import HTTPException

from app.models.purchase_model import Purchase
from app.models.supplier_model import Supplier
from app.models.item_model import Item
from app.schemas.purchase_schema import PurchaseCreate
from app.utils.helper import doc_to_dict


async def create_purchase(data: PurchaseCreate) -> dict:
    try:
        supplier = await Supplier.get(PydanticObjectId(data.supplier_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid supplier ID")
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    try:
        item = await Item.get(PydanticObjectId(data.item_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item ID")
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    purchase = Purchase(
        supplier_id=data.supplier_id,
        item_id=data.item_id,
        supplier_name=supplier.supplier_name,
        item_name=item.item_name,
        purchase_quantity=data.purchase_quantity
    )
    await purchase.insert()

    item.quantity += data.purchase_quantity
    item.updated_at = datetime.now(timezone.utc)
    await item.save()

    return doc_to_dict(purchase)


async def get_all_purchases() -> list:
    purchases = await Purchase.find_all().sort([("created_at", -1)]).to_list()
    return [doc_to_dict(p) for p in purchases]


async def get_purchase(purchase_id: str) -> dict:
    try:
        purchase = await Purchase.get(PydanticObjectId(purchase_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid purchase ID")
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return doc_to_dict(purchase)
