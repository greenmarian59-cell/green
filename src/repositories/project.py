from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload

from src.database.models import Project, UserProject, ProjectImage
from src.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    model = Project

    async def get_by_title(self, session: AsyncSession, title: str) -> Project | None:
        stmt = select(self.model)

        stmt = stmt.where(self.model.title == title)

        return await session.scalar(stmt)



class UserProjectRepository(BaseRepository[UserProject]):
    model = UserProject

    async def get_all_by_user(self, session: AsyncSession, user_id: int) -> List[Project]:
        stmt = select(self.model)

        stmt = stmt.where(self.model.user_id == user_id).options(selectinload(self.model.project).options(selectinload(Project.images)))
        result = await session.execute(stmt)
        projects = result.scalars().all()
        return [item.project for item in projects]

    async def check_project_owner(self, session: AsyncSession, user_id: int) -> UserProject | None:
        stmt = select(self.model)
        stmt = stmt.where(self.model.user_id == user_id).options(selectinload(self.model.project))
        result = await session.execute(stmt)
        return result.scalar()

    async def delete(self, session: AsyncSession, obj):
        await session.delete(obj)
        await session.flush()  # или commit, если требуется


class ProjectImageRepository(BaseRepository[ProjectImage]):
    model = ProjectImage


