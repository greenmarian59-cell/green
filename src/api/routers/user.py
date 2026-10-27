from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, Body, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependancies import get_user_service, get_current_user
from src.core.security import hash_password
from src.database.models import User
from src.database.session import get_session
from src.schemas.auth_schema import TokenSchema
from src.schemas.user import UserBase, UserUpdate, UserCreate, UserLogin, UserFilter
from src.services.user import UserService

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/", response_model=list[UserBase])
async def get_fashion(
        session: AsyncSession = Depends(get_session),
        service: UserService = Depends(get_user_service),
):
    return await service.get_fashion(session=session)

@router.post("/registration", response_model=TokenSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
        payload: UserCreate = Body(...),
        session: AsyncSession = Depends(get_session),
        service: UserService = Depends(get_user_service),
):
    payload_dump = payload.model_dump(exclude_unset=True)
    payload_dump["password"] = hash_password(payload_dump.get("password"))
    db_user = User(**payload_dump)
    new_user = await service.create(session=session, obj=db_user)
    return new_user

@router.post("/login", response_model=TokenSchema, status_code=status.HTTP_201_CREATED)
async def login_user(
        payload: UserLogin,
        # filters: UserFilter = Query(None),
        session: AsyncSession = Depends(get_session),
        service: UserService = Depends(get_user_service),
):
    return await service.login(session=session, obj=payload)

@router.get("/me", response_model=UserBase, status_code=status.HTTP_200_OK)
async def get_user_by_id(
        current_user: User = Depends(get_current_user),
):
    return current_user


@router.patch("/update", response_model=UserBase, status_code=status.HTTP_200_OK)
async def update_user(
        name: str | None = Form(None),
        about: str | None = Form(None),
        photo: UploadFile | None = File(None),
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        service: UserService = Depends(get_user_service),
):
    updated_user = UserUpdate.model_validate({
        "name": name,
        "about": about,
        "photo": photo,
    })
    user_id = current_user.id
    return await service.update(session, user_id, updated_user)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        service: UserService = Depends(get_user_service),
):
    user_id = current_user.id
    return await service.delete(session, user_id)
