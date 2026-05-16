from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded

from app.config.database import connect_to_mongodb, disconnect_from_mongodb
from app.config.settings import settings
from app.middleware.rate_limit import limiter, rate_limit_handler
from app.routes.auth_routes import router as auth_router
from app.routes.supplier_routes import router as supplier_router
from app.routes.item_routes import router as item_router
from app.routes.purchase_routes import router as purchase_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()
    yield
    await disconnect_from_mongodb()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for managing inventory, suppliers, and purchases.",
    lifespan=lifespan
)

app.state.limiter = limiter

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router)
app.include_router(supplier_router)
app.include_router(item_router)
app.include_router(purchase_router)

app.add_exception_handler(RateLimitExceeded, rate_limit_handler)


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    errors = [{"field": " -> ".join(str(l) for l in e["loc"]), "message": e["msg"]} for e in exc.errors()]
    return JSONResponse(status_code=422, content={
        "success": False,
        "message": "Validation error",
        "data": errors,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


@app.get("/", tags=["Health"])
async def root():
    return {"success": True, "message": f"{settings.APP_NAME} is running", "docs": "/docs"}
