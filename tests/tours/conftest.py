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
    return {'name': 'test_activity'}

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

