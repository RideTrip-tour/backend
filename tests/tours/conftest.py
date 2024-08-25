from random import randint

import pytest
import pytest_asyncio
from faker import Faker
from sqlalchemy import insert
from tests.consts import AMOUNT_ITEMS_FOR_TEST

from src.core.tours import models

fk = Faker("ru_RU")


@pytest.fixture
def country_data() -> dict:
    """Возвращает данные тестовой страны"""
    return {"name": "test_country"}


@pytest_asyncio.fixture
async def country(session, country_data):
    """Создает и возвращает объект тестовой страны"""
    country = models.Country(**country_data)
    session.add(country)
    await session.commit()
    await session.refresh(country)
    return country


@pytest.fixture
def activity_data() -> dict:
    """Возвращает данные тестовой активности"""
    return {"name": "test_activity"}


@pytest_asyncio.fixture
async def activity(session, activity_data) -> models.Activity:
    """Создает и возвращает объект Активности"""
    activity = models.Activity(**activity_data)
    session.add(activity)
    await session.commit()
    await session.refresh(activity)
    return activity


@pytest_asyncio.fixture
async def activity_with_locations(
    session, activities_locations_table_add_row, activity
) -> models.Activity:
    """Возвращает активность со связанными локациями"""
    await session.refresh(
        activity,
        [
            "locations",
        ],
    )
    return activity


@pytest_asyncio.fixture
async def list_activities(session) -> None:
    """Добавляет список активностей в БД"""
    activities = [
        models.Activity(name=f"activity_{i}")
        for i in range(AMOUNT_ITEMS_FOR_TEST)
    ]
    session.add_all(activities)
    await session.commit()


@pytest.fixture
def location_data_with_country_id(country) -> dict:
    """Возвращает данные тестовой локации"""
    return {"name": "test_location", "country_id": country.id}


@pytest.fixture
def location_data_with_country_row(country, country_data) -> dict:
    """Возвращает данные тестовой локации"""
    return {
        "name": "test_location",
        "country": {"id": country.id, **country_data},
    }


@pytest_asyncio.fixture
async def location(session, location_data_with_country_id) -> models.Location:
    """Возвращает тестовую локацию"""
    location = models.Location(**location_data_with_country_id)
    session.add(location)
    await session.commit()
    await session.refresh(
        location,
        [
            "country",
        ],
    )
    return location


@pytest_asyncio.fixture
async def location_with_activity(
    session, activities_locations_table_add_row, location
) -> models.Location:
    """Возвращает тестовую локацию с активностями"""
    await session.refresh(
        location,
        [
            "activities",
        ],
    )
    return location


@pytest_asyncio.fixture
async def list_locations(session, country) -> None:
    """Создает список тестовых локаций"""
    locations = [
        models.Location(
            name=f"location_{i}",
            country_id=country.id,
        )
        for i in range(AMOUNT_ITEMS_FOR_TEST)
    ]
    session.add_all(locations)
    await session.commit()


@pytest_asyncio.fixture
async def activities_locations(
    session, list_locations, list_activities, location, activity
) -> list[dict]:
    """Создает связи локаций и активностей.
    Минимум AMOUNT_ITEMS_FOR_TEST // 2 - 1 связей
    Минимум записей AMOUNT_ITEMS_FOR_TEST"""
    r: int = AMOUNT_ITEMS_FOR_TEST
    datas: set[tuple[int, int]] = set()
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

    values: list[dict] = []
    for data in datas:
        values.append({"location_id": data[0], "activity_id": data[1]})
    stmt = insert(models.activities_locations_table).values(values)
    await session.execute(stmt)
    await session.commit()
    return values


@pytest_asyncio.fixture
async def activities_locations_table_add_row(
    session, activity, location
) -> None:
    """Создает связь тестовой локации с тестовой активностью"""
    stmt = insert(models.activities_locations_table).values(
        activity_id=activity.id,
        location_id=location.id,
    )
    await session.execute(stmt)
    await session.commit()


@pytest_asyncio.fixture
async def list_tours(
    session, activities_locations, list_trips, list_accommodations
) -> list[models.Tour]:
    """Создает список туров"""
    tours = [
        models.Tour(
            description=f"big instruction with details tour{i}",
            activity_id=activities_locations[i].get("activity_id"),
            target_location_id=activities_locations[i].get("location_id"),
            start_location_id=i + 1,
            departure_trip_id=i + 1,
            return_trip_id=AMOUNT_ITEMS_FOR_TEST - i,
            accommodation_id=i + 1,
        )
        for i in range(AMOUNT_ITEMS_FOR_TEST)
    ]
    session.add_all(tours)
    await session.commit()
    return tours


@pytest_asyncio.fixture
async def list_trips(session, activities_locations) -> None:
    """Создает список поездок"""
    trips = [
        models.Trip(
            start_at=fk.date_time_this_month(before_now=True),
            finish_at=fk.date_time_this_month(after_now=True),
            target_location_id=activities_locations[i].get("location_id"),
            start_location_id=i + 1,
        )
        for i in range(AMOUNT_ITEMS_FOR_TEST)
    ]
    session.add_all(trips)
    await session.commit()


@pytest_asyncio.fixture
async def list_accommodations(
    session, list_locations, accommodation_type
) -> None:
    """Создает список вариантов проживания"""
    accommodations = [
        models.Accommodation(
            accommodation_type_id=accommodation_type.id,
            checkin_at=fk.date_time_this_month(before_now=True),
            checkout_at=fk.date_time_this_month(after_now=True),
            location_id=i + 1,
            price=fk.random_int(100, 10000),
        )
        for i in range(AMOUNT_ITEMS_FOR_TEST)
    ]
    session.add_all(accommodations)
    await session.commit()


@pytest_asyncio.fixture
async def accommodation_type(session):
    """Создает тип варианта проживания"""
    accommodation_type = models.AccommodationType(name=fk.name_nonbinary())
    session.add(accommodation_type)
    await session.commit()
    await session.refresh(accommodation_type)
    return accommodation_type


@pytest_asyncio.fixture
async def tour(session, list_tours):
    tour = await session.get(models.Tour, 1)
    return tour
