import re

from fastapi import HTTPException

from src.core.exceptions import NotFoundError, UnauthorizedError, ConflictError
from src.core.security import verify_password
from src.database.models import User
from src.repositories.user import UserRepository
from src.schemas.auth_schema import TokenSchema
from src.schemas.user import UserUpdate, UserLogin, UserFilter, UserBase
from src.services.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.files import save_image, delete_file


class UserService(BaseService[User]):
    def __init__(self, repository: UserRepository) -> None:
        super().__init__(repository)

    async def get_fashion(self, session: AsyncSession):
        return await self.repository.get_fashion_with_photo(session)

    async def login(self, session: AsyncSession, obj:UserLogin) -> User:
        exists_phone_number = await self.repository.get_user_by_phone_number(session, obj.phone_number)

        if not exists_phone_number:
            raise NotFoundError(detail="Phone number not exists")

        if not verify_password(obj.password, exists_phone_number.password):
            raise UnauthorizedError(detail="Password incorrect")

        return await self._issue_tokens(exists_phone_number.id)

    # async def filter_login(self, session: AsyncSession, filters:UserFilter):
    #     return await self.repository.get_login_with_filter(session=session, filters=filters)

    async def create(self, session: AsyncSession, obj: User) -> TokenSchema:
        exists_phone_number = await self.repository.get_user_by_phone_number(session, obj.phone_number)
        if not re.match(r"^\+998\d{9}$", obj.phone_number):
            raise HTTPException(
                status_code=400, detail="Неправильный формат номера телефона (+998XXXXXXXXX)"
            )
        if exists_phone_number:
            raise ConflictError(detail="Phone number already exists")

        user = await self.repository.create(session, obj)
        await session.commit()
        await session.refresh(user)

        return await self._issue_tokens(user.id)

    async def update(self, session: AsyncSession, id: int, obj: UserUpdate) -> User:
        user = await self.repository.get(session, id)

        if not user:
            raise NotFoundError(detail="Category not found")

        update_data = obj.model_dump(exclude_unset=True)

        if update_data.get("photo"):
            delete_file(user.photo)
            update_data["photo"] = await save_image(update_data["photo"])

        for field, value in update_data.items():
            setattr(user, field, value)

        updated_obj = await self.repository.update(session, user)
        await session.commit()
        await session.refresh(updated_obj)
        return updated_obj

    async def delete(self, session: AsyncSession, id: int) -> None:
        user = await self.repository.get(session, id)
        if not user:
            raise NotFoundError(detail="User not found")

        await self.repository.delete(session, user)
        delete_file(user.photo)
