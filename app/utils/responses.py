from typing import Any


def success_response(data: Any, message: str = "Success") -> dict:
    return {
        "success": True,
        "message": message,
        "data": data,
    }