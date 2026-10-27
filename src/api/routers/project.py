from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Project, User
from src.api.dependancies import get_project_service, get_current_user
from src.schemas.project_schema import ProjectBase, ProjectCreate, ProjectUpdate, ProjectImage
from src.services.project import ProjectBaseService
from src.database.session import get_session
from src.utils.files import save_image

router = APIRouter(prefix="/project", tags=["Project"])

@router.get("/", response_model=list[ProjectBase])
async def get_all_project(
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user),
        service: ProjectBaseService = Depends(get_project_service),
):
    return await service.get_all_by_user(session=session, user_id=current_user.id)

@router.post("/images/{project_id}", status_code=status.HTTP_201_CREATED)
async def create_project_images(
        project_id: int,
        images: List[UploadFile] = File(),
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        service: ProjectBaseService = Depends(get_project_service),
):


    return await service.create_images(session=session, obj=images, project_id=project_id)


@router.post("/", response_model=ProjectBase, status_code=status.HTTP_201_CREATED)
async def create_project(
        payload: ProjectCreate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        service: ProjectBaseService = Depends(get_project_service),
):
    db_project = Project(**payload.model_dump())
    new_project = await service.create(session=session, obj=db_project, user=current_user)
    return new_project

@router.post("/star", status_code=status.HTTP_200_OK)
async def create_star(
        project_id: int,
        request: Request,
        session: AsyncSession = Depends(get_session),
        service: ProjectBaseService = Depends(get_project_service),
):
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent")
    return {"client": client_ip, "user_agent": user_agent}

@router.get("/{project_id}", response_model=ProjectBase, status_code=status.HTTP_200_OK)
async def get_project_by_id(
        project_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        service: ProjectBaseService = Depends(get_project_service),
):
    return await service.get(session, project_id)


@router.put("/{project_id}", response_model=ProjectBase, status_code=status.HTTP_200_OK)
async def update_project(
        payload: ProjectUpdate,
        project_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        service: ProjectBaseService = Depends(get_project_service),
):
    user_id = current_user.id
    return await service.update(session, project_id, payload, user_id)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
        project_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        service: ProjectBaseService = Depends(get_project_service),
):
    return await service.delete(session, project_id)


