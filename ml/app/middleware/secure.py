from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import os

# Читаем из окружения
SERVICE_KEY = os.getenv("SERVICE_API_KEY")
if not SERVICE_KEY:
    raise RuntimeError("SERVICE_API_KEY not set")

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/health":
            return await call_next(request)
        
        if request.headers.get("X-API-KEY") != SERVICE_KEY:
            # Возвращаем JSONResponse вместо исключения
            return JSONResponse(
                status_code=403,
                content={"detail": "Forbidden"}
            )
        
        return await call_next(request)