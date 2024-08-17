from random import randint

import pytest
import pytest_asyncio
from sqlalchemy import insert
from tests.consts import AMOUNT_ITEMS_FOR_TEST

from src.v1.tours import models


@pytest.fixture
def activity_data() -> dict:
    return {"name": "test_activity"}


@pytest_asyncio.fixture
async def activity(session, activity_data):
    """Создает и возвращает модель Активности"""
    activity = models.Activity(**activity_data)
    session.add(activity)
    await session.commit()
    await session.refresh(activity)
    return activity


@pytest_asyncio.fixture
async def activity_with_locations(
    session, activities_locations_table_add_row, activity
):
    """"""
    await session.refresh(
        activity,
        [
            "locations",
        ],
    )
    return activity


@pytest.fixture
def activity_data_with_locations(activity_data, location_data, location):
    return {
        **activity_data,
        "locations": [{"id": location.id, **location_data}],
    }


@pytest_asyncio.fixture
async def list_activities(session):
    activities = [
        models.Activity(name=f"activity_{i}")
        for i in range(AMOUNT_ITEMS_FOR_TEST)
    ]
    session.add_all(activities)
    await session.commit()


@pytest.fixture
def location_data():
    return {"name": "test_location"}


@pytest_asyncio.fixture
async def location(session, location_data):
    location = models.Location(**location_data)
    session.add(location)
    await session.commit()
    await session.refresh(location)
    return location


@pytest_asyncio.fixture
async def location_with_activity(
    session, activities_locations_table_add_row, location
):
    await session.refresh(
        location,
        [
            "activities",
        ],
    )
    return location


@pytest.fixture
def location_data_with_activity(activity_data, location_data, activity):
    return {
        **location_data,
        "activities": [{"id": activity.id, **activity_data}],
    }


@pytest_asyncio.fixture
async def list_locations(session):
    locations = [
        models.Location(name=f"location_{i}")
        for i in range(AMOUNT_ITEMS_FOR_TEST)
    ]
    session.add_all(locations)
    await session.commit()


@pytest_asyncio.fixture
async def activities_locations(
    session, list_locations, list_activities, location, activity
):
    r: int = AMOUNT_ITEMS_FOR_TEST
    datas = set()
    for i in range(1, (r // 2)):
        data_loc = (location.id, i)
        data_act = (i, activity.id)
        datas.update(
            (
                data_loc,
                data_act,
            )
        )

    while len(datas) < r:
        data = (
            randint(1, r),  # loc_id
            randint(1, r),  # activ_id
        )
        datas.add(data)

    for data in datas:
        stmt = insert(models.activities_locations_table).values(
            {"location_id": data[0], "activity_id": data[1]}
        )
        await session.execute(stmt)
    await session.commit()


@pytest_asyncio.fixture
async def activities_locations_table_add_row(session, activity, location):
    stmt = insert(models.activities_locations_table).values(
        activity_id=activity.id,
        location_id=location.id,
    )
    await session.execute(stmt)
    await session.commit()
