from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.database.models.client_ip import ClientIp
from src.repositories.base import BaseRepository


class ClientIpRepository(BaseRepository[ClientIp]):
    model = ClientIp

    async def get(self, session:AsyncSession, obj:ClientIp) -> ClientIp | None:
        stmt = select(self.model)

        stmt = stmt.where(
           and_(
               self.model.project_id == obj.project_id,
               self.model.user_agent == obj.user_agent,
               self.model.client == obj.client
           )
        )
        project = await session.scalar(stmt)
        return project