from datetime import datetime, timezone
from typing import Any, Optional


def ok(message: str, data: Any = None) -> dict:
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def fail(message: str, error_code: Optional[str] = None, data: Any = None) -> dict:
    return {
        "success": False,
        "message": message,
        "error_code": error_code,
        "data": data,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
