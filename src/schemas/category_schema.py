from datetime import datetime

from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    id: int
    name: str

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(CategoryCreate):
    pass