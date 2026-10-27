from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings

# Async engine yaratish
engine = create_async_engine(settings.database_url, echo=settings.db_echo)

# Async session factory
SessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,  # Async'da commit'dan keyin obyekt atributlariga kirishda xatolik bermasligi uchun
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session