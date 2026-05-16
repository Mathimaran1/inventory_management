from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from app.services import supplier_service
from app.utils.helper import get_current_user
from app.utils.response_handler import ok
from app.schemas.supplier_schema import SupplierCreate, SupplierUpdate
from app.middleware.rate_limit import limiter

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.post("/", status_code=201, summary="Create supplier")
@limiter.limit("20/minute")
async def create(request: Request, data: SupplierCreate, _=Depends(get_current_user)):
    result = await supplier_service.create_supplier(data)
    return ok("Supplier created", result)


@router.get("/", summary="Get all suppliers")
@limiter.limit("20/minute")
async def get_all(request: Request, city: Optional[str] = Query(None, description="Filter by city"), _=Depends(get_current_user)):
    result = await supplier_service.get_all_suppliers(city)
    return ok("Suppliers fetched", result)


@router.get("/{supplier_id}", summary="Get supplier by ID")
@limiter.limit("20/minute")
async def get_one(request: Request, supplier_id: str, _=Depends(get_current_user)):
    result = await supplier_service.get_supplier(supplier_id)
    return ok("Supplier fetched", result)


@router.put("/{supplier_id}", summary="Update supplier")
@limiter.limit("20/minute")
async def update(request: Request, supplier_id: str, data: SupplierUpdate, _=Depends(get_current_user)):
    result = await supplier_service.update_supplier(supplier_id, data)
    return ok("Supplier updated", result)


@router.delete("/{supplier_id}", summary="Delete supplier")
@limiter.limit("20/minute")
async def delete(request: Request, supplier_id: str, _=Depends(get_current_user)):
    result = await supplier_service.delete_supplier(supplier_id)
    return ok("Supplier deleted", result)
