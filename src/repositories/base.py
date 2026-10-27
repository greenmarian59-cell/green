from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    async def get(self, session: AsyncSession, pk: int) -> ModelType | None:
        return await session.get(self.model, pk)

    async def get_all(self, session: AsyncSession) -> list[ModelType]:
        result = await session.execute(select(self.model))
        get_all = result.scalars().all()
        return list(get_all)

    async def create(self, session: AsyncSession, obj: ModelType) -> ModelType:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def update(self, session: AsyncSession, obj: ModelType) -> ModelType:
        await  session.commit()
        await session.refresh(obj)
        return obj

    async def delete(self, session: AsyncSession, obj: ModelType) -> None:
        await session.delete(obj)
        await session.commit()