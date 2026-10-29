from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.database.base import Base


class ClientIp(Base):
    __tablename__ = "client_ip"

    id: Mapped[int] = mapped_column(primary_key=True)
    client: Mapped[str] = mapped_column(String, nullable=False)
    user_agent: Mapped[str] = mapped_column(String, nullable=False)
    project_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

