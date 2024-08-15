import pytest
import pytest_asyncio
from sqlalchemy import insert, select

from src.v1.tours import models
from tests.tours.consts import AMOUNT_ITEMS_FOR_TEST


@pytest.fixture
def activity_data():
    return {'name': 'test_activity'}

@pytest_asyncio.fixture
async def activity(session, activity_data):
    stmt = insert(models.activity).values(**activity_data)
    await session.execute(stmt)
    await session.commit()

    query = models.activity.select()
    result = await session.execute(query)
    return result.first()

@pytest_asyncio.fixture
async def list_activities(session):
    stmt = insert(models.activity).values([{'name': f'activity_{i}'} for i in range(AMOUNT_ITEMS_FOR_TEST)])
    await session.execute(stmt)
    await session.commit()


@pytest.fixture
def location_data():
    return {'name': 'test_activity'}

@pytest_asyncio.fixture
async def location(session, location_data):
    stmt = insert(models.location).values(**location_data)
    await session.execute(stmt)
    await session.commit()

    query = select(models.location)
    result = await session.execute(query)
    return result.first()

@pytest_asyncio.fixture
async def list_locations(session, activity, list_activities):
    stmt = insert(models.location).values([{'name': f'location_{i}', "activity_id": i+1} for i in range(AMOUNT_ITEMS_FOR_TEST)])
    await session.execute(stmt)
    await session.commit()