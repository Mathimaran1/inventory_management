from fastapi import APIRouter, Depends, Request
from app.services import auth_service
from app.utils.helper import get_current_user
from app.utils.response_handler import ok
from app.schemas.auth_schema import UserRegister, UserLogin
from app.middleware.rate_limit import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201, summary="Register a new user")
@limiter.limit("5/minute")
async def register(request: Request, data: UserRegister):
    result = await auth_service.register_user(data)
    return ok("Registered successfully", result)


@router.post("/login", summary="Login and get JWT token")
@limiter.limit("5/minute")
async def login(request: Request, data: UserLogin):
    result = await auth_service.login_user(data)
    return ok("Login successful", result)


@router.get("/me", summary="Get current user profile")
@limiter.limit("20/minute")
async def me(request: Request, current_user: dict = Depends(get_current_user)):
    result = await auth_service.get_user_profile(current_user["sub"])
    return ok("Profile fetched", result)
