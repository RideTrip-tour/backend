from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.database import DATABASE_URL, Base, get_async_session
from src.main import app

DATABASE_URL_TEST = DATABASE_URL._replace(database="rtt_test")


@pytest_asyncio.fixture
async def async_session_maker(async_db_connection):
    yield async_sessionmaker(async_db_connection, expire_on_commit=False)


@pytest_asyncio.fixture
async def session(async_session_maker, async_db_connection):
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture()
async def app_test(async_db_connection, async_session_maker):
    async def get_async_session_test() -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session

    app.dependency_overrides[get_async_session] = get_async_session_test
    yield app


@pytest_asyncio.fixture(scope="function")
async def async_db_connection():
    engine = create_async_engine(
        DATABASE_URL_TEST,
    )
    # Создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with engine.connect() as conn:
        try:
            yield conn
        except Exception as ex:
            raise ex
        finally:
            await conn.rollback()

    # Удаление таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture()
async def client(app_test) -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app_test), base_url="http://localhost"
    ) as client:
        yield client
