from datetime import datetime

from pydantic import BaseModel, Field
from fastapi import UploadFile


class UserBase(BaseModel):
    id: int
    name: str
    phone_number: str
    about: str | None
    photo: str | None

class UserCreate(BaseModel):
    name: str
    phone_number: str
    about: str | None = Field(None)
    password: str

class UserUpdate(BaseModel):
    name: str
    about: str | None
    photo: UploadFile | None

class UserLogin(BaseModel):
    phone_number: str
    password: str

class UserFilter(BaseModel):
    phone_number: str
