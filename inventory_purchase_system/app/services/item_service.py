from datetime import datetime, timezone
from typing import Optional

from beanie import PydanticObjectId
from fastapi import HTTPException

from app.models.item_model import Item
from app.schemas.item_schema import ItemCreate, ItemUpdate
from app.utils.helper import doc_to_dict


def _to_dict(item: Item) -> dict:
    d = doc_to_dict(item)
    d["is_low_stock"] = item.is_low_stock
    return d


async def _get_or_404(item_id: str) -> Item:
    try:
        item = await Item.get(PydanticObjectId(item_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item ID")
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


async def create_item(data: ItemCreate) -> dict:
    if await Item.find_one(Item.item_name == data.item_name):
        raise HTTPException(status_code=409, detail="Item already exists")
    item = Item(**data.model_dump())
    await item.insert()
    return _to_dict(item)


async def get_all_items(category: Optional[str] = None) -> list:
    query = {"category": {"$regex": category, "$options": "i"}} if category else {}
    items = await Item.find(query).to_list()
    return [_to_dict(i) for i in items]


async def get_item(item_id: str) -> dict:
    return _to_dict(await _get_or_404(item_id))


async def update_item(item_id: str, data: ItemUpdate) -> dict:
    item = await _get_or_404(item_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(item, field, value)
    item.updated_at = datetime.now(timezone.utc)
    await item.save()
    return _to_dict(item)


async def delete_item(item_id: str) -> dict:
    item = await _get_or_404(item_id)
    await item.delete()
    return {"deleted_id": item_id}


async def reduce_stock(item_id: str, reduce_by: int) -> dict:
    item = await _get_or_404(item_id)
    if item.quantity < reduce_by:
        raise HTTPException(status_code=400, detail=f"Not enough stock. Available: {item.quantity}")
    item.quantity -= reduce_by
    item.updated_at = datetime.now(timezone.utc)
    await item.save()
    return _to_dict(item)


async def stock_summary() -> dict:
    items = await Item.find_all().to_list()
    categories = {}
    for item in items:
        cat = item.category
        if cat not in categories:
            categories[cat] = {"item_count": 0, "total_units": 0, "total_value": 0.0}
        categories[cat]["item_count"] += 1
        categories[cat]["total_units"] += item.quantity
        categories[cat]["total_value"] += round(item.price * item.quantity, 2)

    return {
        "total_items": len(items),
        "total_units": sum(i.quantity for i in items),
        "total_value": round(sum(i.price * i.quantity for i in items), 2),
        "low_stock_count": sum(1 for i in items if i.is_low_stock),
        "by_category": list(categories.values())
    }


async def low_stock_items() -> list:
    items = await Item.find({"$expr": {"$lte": ["$quantity", "$reorder_level"]}}).to_list()
    return [_to_dict(i) for i in items]
