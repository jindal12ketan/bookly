from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.config import Config
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(Config.DATABASE_URL, echo=True)
# async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    from src.db.models import Book  # ensure models are imported

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


from typing import AsyncGenerator


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as session:
        yield session
