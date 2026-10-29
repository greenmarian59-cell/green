import jwt
from fastapi import Security, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.exceptions import NotFoundError
from src.core.security import get_user_id_from_token
from src.database.models import User
from src.database.session import get_session
from src.repositories.category import CategoryRepository
from src.repositories.client_ip import ClientIpRepository
from src.repositories.project import ProjectRepository, UserProjectRepository, ProjectImageRepository
from src.repositories.user import UserRepository
from src.services.category import CategoryService
from src.services.client_ip import ClientIpService
from src.services.project import ProjectBaseService
from src.services.user import UserService

user_access_token_scheme = HTTPBearer(scheme_name="user-access-token", auto_error=True)


def get_category_service() -> CategoryService:
    repository = CategoryRepository()
    return CategoryService(repository)

def get_client_ip_service() -> ClientIpService:
    repository = ClientIpRepository()
    project_repo = ProjectRepository()
    return ClientIpService(repository, project_repo)


def get_user_service() -> UserService:
    repository = UserRepository()
    return UserService(repository)

def get_project_service() -> ProjectBaseService:
    project_repo = ProjectRepository()
    user_project_repo = UserProjectRepository()
    project_image_repo = ProjectImageRepository()
    return ProjectBaseService(project_repo, user_project_repo, project_image_repo)


async def get_current_user(
        credentials: HTTPAuthorizationCredentials | None = Security(user_access_token_scheme),
        session: AsyncSession = Depends(get_session),
        service: UserService = Depends(get_user_service)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid or expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_exception

    try:
        user_id = await get_user_id_from_token(credentials.credentials)
    except jwt.PyJWTError as exc:
        raise credentials_exception

    try:
        user = await service.get(session=session, pk=user_id)
    except NotFoundError:
        raise credentials_exception

    return user
