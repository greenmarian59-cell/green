from typing import List

from fastapi import HTTPException, UploadFile

from src.core.exceptions import NotFoundError, ConflictError
from src.database.models import User
from src.database.models.client_ip import ClientIp
from src.database.models.project import Project, UserProject, ProjectImage
from src.repositories.project import ProjectRepository, UserProjectRepository, ProjectImageRepository
from src.schemas.project_schema import ProjectUpdate, ProjectDefaultResponse
from src.services.base import BaseService, ModelType
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.files import save_image, delete_file


class ProjectBaseService(BaseService[Project]):
    def __init__(
        self,
        project_repo: ProjectRepository,
        user_project_repo: UserProjectRepository,
        project_image_repo: ProjectImageRepository
    ) -> None:
        self.project_repo = project_repo
        self.user_project_repo = user_project_repo
        self.project_image_repo = project_image_repo
        super().__init__(project_repo)

    async def get_all_by_user(self, session:AsyncSession, user_id: int) -> List[Project]:
        return await self.user_project_repo.get_all_by_user(session, user_id)

    async def create(self, session: AsyncSession, obj: Project, user: User) -> Project:

        check_title = await self.project_repo.get_by_title(session, obj.title)
        if check_title:
            raise ConflictError(f"Project with title {check_title.title} already exists")

        new_project = await self.project_repo.create(session, obj)
        user_project_obj = UserProject(**{"user_id": user.id, "project_id": new_project.id})
        await self.user_project_repo.create(session, user_project_obj)
        await session.commit()
        return new_project

    async def update(self, session: AsyncSession, project_id: int, obj:ProjectUpdate, user_id: int) -> Project:
        user_project = await self.user_project_repo.check_project_owner(session, user_id)
        if user_project is None:
            raise NotFoundError(f"User with id {user_id} does not exist")
        if user_project.project_id != project_id:
            raise ConflictError(f"User has no id:{project_id} project")
        project = user_project.project

        for field, value in obj.model_dump(exclude_unset=True).items():
            setattr(project, field, value)
        project_update = await self.project_repo.update(session, project)
        await session.commit()
        await session.refresh(project_update)
        return project_update

    async def delete(self, session: AsyncSession, id: int):
        obj = await self.user_project_repo.get(session, id)

        if not obj:
            raise HTTPException(status_code=404, detail="Project not found")

        await self.user_project_repo.delete(session, obj)
        await session.commit()
        return obj

    async def create_images(self, session: AsyncSession, obj:List[UploadFile], project_id: int) -> ProjectDefaultResponse | None:
        check_project = await self.project_repo.check_project(session, project_id)
        if check_project is None:
            raise NotFoundError(f"Project with id {project_id} does not exist")
        # new_images = []
        # for image in obj:
        #     new_images.append(save_image(image))
        # obj = ProjectImage(**{"project_id": project_id, "images": new_images})
        # await self.project_image_repo.create(session, obj)
        if check_project.images:
            for item in check_project.images:
                delete_file(item.image)
                await self.project_image_repo.delete(session, item)

        for image in obj:
            new_image = await save_image(image)
            result = ProjectImage(**{"project_id": project_id, "image": new_image})
            await self.project_image_repo.create(session, result)
            await session.commit()

        return ProjectDefaultResponse(massage="Project created successfully")







