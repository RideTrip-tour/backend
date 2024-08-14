from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from scr.config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

metadata = MetaData()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

