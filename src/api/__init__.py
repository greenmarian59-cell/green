from fastapi import APIRouter
from src.api.routers.categories import router as categories_router
from src.api.routers.user import router as user_router
from src.api.routers.project import router as project_router



main_router = APIRouter()

main_router.include_router(categories_router)
main_router.include_router(user_router)
main_router.include_router(project_router)