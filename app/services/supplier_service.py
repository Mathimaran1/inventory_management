from datetime import datetime, timezone
from typing import Optional

from beanie import PydanticObjectId
from fastapi import HTTPException

from app.models.supplier_model import Supplier
from app.schemas.supplier_schema import SupplierCreate, SupplierUpdate
from app.utils.helper import doc_to_dict


async def create_supplier(data: SupplierCreate) -> dict:
    if await Supplier.find_one(Supplier.supplier_name == data.supplier_name):
        raise HTTPException(status_code=409, detail="Supplier already exists")
    supplier = Supplier(**data.model_dump())
    await supplier.insert()
    return doc_to_dict(supplier)


async def get_all_suppliers(city: Optional[str] = None) -> list:
    query = {"city": {"$regex": city, "$options": "i"}} if city else {}
    suppliers = await Supplier.find(query).to_list()
    return [doc_to_dict(s) for s in suppliers]


async def get_supplier(supplier_id: str) -> dict:
    try:
        supplier = await Supplier.get(PydanticObjectId(supplier_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid supplier ID")
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return doc_to_dict(supplier)


async def update_supplier(supplier_id: str, data: SupplierUpdate) -> dict:
    try:
        supplier = await Supplier.get(PydanticObjectId(supplier_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid supplier ID")
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(supplier, field, value)
    supplier.updated_at = datetime.now(timezone.utc)
    await supplier.save()
    return doc_to_dict(supplier)


async def delete_supplier(supplier_id: str) -> dict:
    try:
        supplier = await Supplier.get(PydanticObjectId(supplier_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid supplier ID")
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    await supplier.delete()
    return {"deleted_id": supplier_id}
