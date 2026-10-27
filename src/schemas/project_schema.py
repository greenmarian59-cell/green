from datetime import datetime
from typing import List

from pydantic import BaseModel, Field
from fastapi import UploadFile



class ProjectBase(BaseModel):
    id: int
    title: str
    description: str
    project_link: str
    category_id: int
    stars: int
    images: List[ProjectImage]


class ProjectCreate(BaseModel):
    title: str
    description: str
    project_link: str
    category_id: int


class ProjectUpdate(ProjectCreate):
    pass

class ProjectImage(BaseModel):
    image: str

