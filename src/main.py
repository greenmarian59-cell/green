from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from src.api import main_router
from src.core.exceptions import AppError

app = FastAPI()
# app.openapi_version = "3.0.2"

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    headers = (
        {"WWW-Authenticate": "Bearer"}
        if exc.status_code == status.HTTP_401_UNAUTHORIZED
        else None
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=headers,
    )

app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(main_router)