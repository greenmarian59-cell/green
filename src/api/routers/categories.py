from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Category
from src.api.dependancies import get_category_service
from src.schemas.category_schema import CategoryBase, CategoryCreate, CategoryUpdate
from src.services.category import CategoryService
from src.database.session import get_session

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryBase])
async def get_all_categories(
        session: AsyncSession = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):
    return await service.get_all(session=session)


@router.post("/", response_model=CategoryBase, status_code=status.HTTP_201_CREATED)
async def create_category(
        payload: CategoryCreate,
        session: AsyncSession = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):
    db_category = Category(**payload.model_dump())
    new_category = await service.create(session=session, obj=db_category)
    return new_category


@router.get("/{category_id}", response_model=CategoryBase, status_code=status.HTTP_200_OK)
async def get_category_by_id(
        category_id: int,
        session: AsyncSession = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):
    return await service.get(session, category_id)


@router.put("/{category_id}", response_model=CategoryBase, status_code=status.HTTP_200_OK)
async def update_category(
        payload: CategoryUpdate,
        category_id: int,
        session: AsyncSession = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):

    return await service.update(session, category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        category_id: int,
        session: AsyncSession = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):
    return await service.delete(session, category_id)

# @router.post("/{category_id}", response_model=CategoryBase, status_code=status.HTTP_201_CREATED)
# def choose_category(
#
# )