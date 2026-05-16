from datetime import datetime, timezone
from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)


async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={
        "success": False,
        "message": "Too many requests. Please slow down.",
        "error_code": "RATE_LIMIT_429",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
