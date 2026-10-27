from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.database.base import Base
if TYPE_CHECKING:
    from src.database.models.project import Project


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    projects: Mapped[List["Project"]] = relationship(back_populates="category")
