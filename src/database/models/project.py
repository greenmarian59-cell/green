from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.models.category import Category
if TYPE_CHECKING:
    from src.database.models.user import User



class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    project_link: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categories.id"), nullable=False)
    stars: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    # Relationships
    category: Mapped["Category"] = relationship(back_populates="projects")
    user_projects: Mapped[List["UserProject"]] = relationship(back_populates="project")
    images: Mapped[List["ProjectImage"]] = relationship(back_populates="project")


class UserProject(Base):
    __tablename__ = "user_projects"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("projects.id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="user_projects")
    project: Mapped["Project"] = relationship(back_populates="user_projects")


class ProjectImage(Base):
    __tablename__ = "project_images"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String, nullable=False)
    project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("projects.id"), nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="images")