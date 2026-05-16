from fastapi import APIRouter, Depends, Request
from app.services import purchase_service
from app.utils.helper import get_current_user
from app.utils.response_handler import ok
from app.schemas.purchase_schema import PurchaseCreate
from app.middleware.rate_limit import limiter

router = APIRouter(prefix="/purchases", tags=["Purchases"])


@router.post("/", status_code=201, summary="Record a purchase")
@limiter.limit("20/minute")
async def create(request: Request, data: PurchaseCreate, _=Depends(get_current_user)):
    result = await purchase_service.create_purchase(data)
    return ok("Purchase recorded", result)


@router.get("/", summary="Get all purchases")
@limiter.limit("20/minute")
async def get_all(request: Request, _=Depends(get_current_user)):
    result = await purchase_service.get_all_purchases()
    return ok("Purchases fetched", result)


@router.get("/{purchase_id}", summary="Get purchase by ID")
@limiter.limit("20/minute")
async def get_one(request: Request, purchase_id: str, _=Depends(get_current_user)):
    result = await purchase_service.get_purchase(purchase_id)
    return ok("Purchase fetched", result)
