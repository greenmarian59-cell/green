from typing import List, Optional
from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.models.project import UserProject


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    about: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    photo: Mapped[str|None] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    user_projects: Mapped[List["UserProject"]] = relationship(back_populates="user")