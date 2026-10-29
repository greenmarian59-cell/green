from src.core.exceptions import NotFoundError, ConflictError
from src.database.models.client_ip import ClientIp
from src.repositories.client_ip import ClientIpRepository
from src.repositories.project import ProjectRepository
from src.schemas.project_schema import ProjectDefaultResponse
from src.services.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession


class ClientIpService(BaseService[ClientIp]):
    def __init__(self, repository: ClientIpRepository, project_repo: ProjectRepository) -> None:
        self.repository = repository
        self.project_repo = project_repo
        super().__init__(repository)

    async def add_star(self, session: AsyncSession, obj: ClientIp) -> ProjectDefaultResponse:
        check_ip = await self.repository.get(session, obj)
        if check_ip:
            raise ConflictError(f"User with this ip already used")

        await self.project_repo.update_star(session, obj.project_id)
        await self.repository.create(session, obj)
        await session.commit()
        return ProjectDefaultResponse(massage="Project created successfully")