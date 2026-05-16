import re
from pydantic import BaseModel, EmailStr, field_validator


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]{3,50}$", v):
            raise ValueError("Username: 3-50 chars, letters/numbers/underscore only")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8 or not re.search(r"[A-Za-z]", v) or not re.search(r"\d", v):
            raise ValueError("Password must be 8+ chars with at least one letter and one digit")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {"username": "john_doe", "email": "john@example.com", "password": "Pass1234"}
        }
    }


class UserLogin(BaseModel):
    username: str
    password: str

    model_config = {
        "json_schema_extra": {"example": {"username": "john_doe", "password": "Pass1234"}}
    }
