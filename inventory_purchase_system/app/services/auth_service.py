from fastapi import HTTPException

from app.models.user_model import User
from app.schemas.auth_schema import UserRegister, UserLogin
from app.config.security import hash_password, verify_password, create_access_token
from app.config.settings import settings
from app.utils.helper import doc_to_dict
from beanie import PydanticObjectId


async def register_user(data: UserRegister) -> dict:
    if await User.find_one(User.username == data.username):
        raise HTTPException(status_code=409, detail="Username already taken")
    if await User.find_one(User.email == data.email):
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(username=data.username, email=data.email, hashed_password=hash_password(data.password))
    await user.insert()

    d = doc_to_dict(user)
    d.pop("hashed_password", None)
    return d


async def login_user(data: UserLogin) -> dict:
    user = await User.find_one(User.username == data.username.lower())
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    token = create_access_token({"sub": str(user.id), "username": user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES
    }


async def get_user_profile(user_id: str) -> dict:
    try:
        user = await User.get(PydanticObjectId(user_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    d = doc_to_dict(user)
    d.pop("hashed_password", None)
    return d
