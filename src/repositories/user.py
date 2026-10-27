from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.database.models import User
from src.repositories.base import BaseRepository, ModelType
from src.schemas.user import UserFilter, UserBase


class UserRepository(BaseRepository[User]):
    model = User

    async def get_fashion_with_photo(self,session: Session) -> list[ModelType]:
        stmt = select(self.model).where(
            self.model.photo.is_not(None),
            self.model.photo != ""
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())


    async def get_user_by_phone_number(
            self, session: AsyncSession, phone_number: str
    ) -> User | None:
        stmt = select(self.model)

        if phone_number is not None:
            stmt = stmt.where(self.model.phone_number == phone_number)

        return await session.scalar(stmt)

    async def update(self, session: Session, obj: User) -> User:
        session.flush()
        return obj

    # async def get_login_with_filter(self, session:Session, filters:UserFilter):
    #     async def get_login_with_filter(self, session: AsyncSession, filters: UserFilter):
    #         stmt = select(self.model).where(self.model.phone_number == filters.phone_number)
    #         result = await session.execute(stmt)
    #         user = result.scalars().first()
    #         if not user:
    #             raise NotFoundError(detail="wrong phone number")
    #         if user.password != filters.password:
    #             raise NotFoundError(detail="wrong password")
    #         return user
