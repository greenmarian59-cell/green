from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import NotFoundError
from src.core.security import create_access_token, create_refresh_token
from src.database.base import Base
from src.repositories.base import BaseRepository
from src.schemas.auth_schema import TokenSchema
ModelType = TypeVar("ModelType", bound=Base)


class BaseService(Generic[ModelType]):
    def __init__(self, repository: BaseRepository[ModelType]) -> None:
        self.repository = repository

    @staticmethod
    async def _issue_tokens(user_id: int) -> TokenSchema:
        return TokenSchema.model_validate(
            {
                "access_token": create_access_token(user_id),
                "refresh_token": create_refresh_token(user_id),
                "token_type": "bearer",
            }
        )

    async def get(self, session: AsyncSession, pk: int) -> ModelType | None:
        return await self.repository.get(session, pk)

    async def get_all(self, session: AsyncSession) -> list[ModelType]:
        return await self.repository.get_all(session)

    async def create(self, session: AsyncSession, obj: ModelType) -> ModelType:
        return await self.repository.create(session, obj)

    async def update(self, session: AsyncSession, obj: ModelType) -> ModelType:
        return await self.repository.update(session, obj)

    async def delete(self, session: AsyncSession, obj: ModelType) -> None:
        await self.repository.delete(session, obj)
