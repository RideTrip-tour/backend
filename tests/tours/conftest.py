from random import randint

import pytest
import pytest_asyncio
from sqlalchemy import insert

from src.v1.tours import models, schemas
from tests.consts import AMOUNT_ITEMS_FOR_TEST


@pytest.fixture
def activity_data():
    return {'name': 'test_activity'}

@pytest_asyncio.fixture
async def activity(session, activity_data):
    activity = models.Activity(**activity_data)
    session.add(activity)
    await session.commit()
    await session.refresh(activity)
    return activity

@pytest_asyncio.fixture
async def list_activities(session):
    activities = [models.Activity(name=f'activity_{i}') for i in range(AMOUNT_ITEMS_FOR_TEST)]
    session.add_all(activities)
    await session.commit()


@pytest.fixture
def location_data():
    return {'name': 'test_location'}

@pytest_asyncio.fixture
async def location(session, location_data):
    location = models.Location(**location_data)
    session.add(location)
    await session.commit()
    await session.refresh(location)
    return location

@pytest_asyncio.fixture
async def list_locations(session):
    locations = [models.Location(name=f'location_{i}') for i in range(AMOUNT_ITEMS_FOR_TEST)]
    session.add_all(locations)
    await session.commit()

@pytest_asyncio.fixture
async def activities_locations(session, list_locations, list_activities, location):
    r: int = AMOUNT_ITEMS_FOR_TEST
    datas = set()
    for i in range(1, (r // 2)):
        data = (location.id, i)
        datas.add(data)

    while len(datas) < r:
        data = (
            randint(1, r), # loc_id
            randint(1, r), # activ_id
        )
        datas.add(data)
    for data in datas:
        stmt = insert(models.activities_locations_table).values(
            {
                'location_id': data[0],
                'activity_id': data[1]
            }
        )
        await session.execute(stmt)
    await session.commit()
