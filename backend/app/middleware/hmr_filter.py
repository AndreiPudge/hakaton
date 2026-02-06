from fastapi import Request
from fastapi.responses import JSONResponse

async def hmr_filter_middleware(request: Request, call_next):
    path = request.url.path
    if "hot-update.json" in path:
        return JSONResponse(
            content={"detail": "Not Found"}, 
            status_code=404
        )
    return await call_next(request)