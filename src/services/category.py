from src.core.exceptions import NotFoundError
from src.database.models.category import Category
from src.repositories.category import CategoryRepository
from src.schemas.category_schema import CategoryUpdate
from src.services.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryService(BaseService[Category]):
    def __init__(self, repository: CategoryRepository) -> None:
        super().__init__(repository)

    async def update(self, session: AsyncSession, id: int, obj: CategoryUpdate) -> Category:
        category = await self.repository.get(session, id)

        if not category:
            raise NotFoundError(detail="Category not found")

        update_data = obj.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(category, field, value)

        updated_obj = await self.repository.update(session, category)
        await session.commit()
        await session.refresh(updated_obj)
        return updated_obj

    async def delete(self, session: AsyncSession, id: int) -> None:
        category = await self.repository.get(session, id)

        if not category:
            raise NotFoundError(detail="Category not found")

        await self.repository.delete(session, category)