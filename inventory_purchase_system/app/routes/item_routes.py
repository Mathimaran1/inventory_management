from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from app.services import item_service
from app.utils.helper import get_current_user
from app.utils.response_handler import ok
from app.schemas.item_schema import ItemCreate, ItemUpdate, StockReduce
from app.middleware.rate_limit import limiter

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", status_code=201, summary="Add inventory item")
@limiter.limit("20/minute")
async def create(request: Request, data: ItemCreate, _=Depends(get_current_user)):
    result = await item_service.create_item(data)
    return ok("Item created", result)


@router.get("/summary", summary="Stock summary")
@limiter.limit("20/minute")
async def summary(request: Request, _=Depends(get_current_user)):
    result = await item_service.stock_summary()
    return ok("Stock summary", result)


@router.get("/low-stock", summary="Low stock items")
@limiter.limit("20/minute")
async def low_stock(request: Request, _=Depends(get_current_user)):
    result = await item_service.low_stock_items()
    return ok("Low stock items", result)


@router.get("/", summary="Get all items")
@limiter.limit("20/minute")
async def get_all(request: Request, category: Optional[str] = Query(None, description="Filter by category"), _=Depends(get_current_user)):
    result = await item_service.get_all_items(category)
    return ok("Items fetched", result)


@router.get("/{item_id}", summary="Get item by ID")
@limiter.limit("20/minute")
async def get_one(request: Request, item_id: str, _=Depends(get_current_user)):
    result = await item_service.get_item(item_id)
    return ok("Item fetched", result)


@router.put("/{item_id}", summary="Update item")
@limiter.limit("20/minute")
async def update(request: Request, item_id: str, data: ItemUpdate, _=Depends(get_current_user)):
    result = await item_service.update_item(item_id, data)
    return ok("Item updated", result)


@router.delete("/{item_id}", summary="Delete item")
@limiter.limit("20/minute")
async def delete(request: Request, item_id: str, _=Depends(get_current_user)):
    result = await item_service.delete_item(item_id)
    return ok("Item deleted", result)


@router.patch("/{item_id}/reduce-stock", summary="Reduce item stock")
@limiter.limit("20/minute")
async def reduce_stock(request: Request, item_id: str, data: StockReduce, _=Depends(get_current_user)):
    result = await item_service.reduce_stock(item_id, data.reduce_by)
    return ok("Stock reduced", result)
