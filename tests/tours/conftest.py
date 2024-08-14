import pytest
import pytest_asyncio

from scr.v1.tours.models import TourORM, LocationORM


@pytest.fixture
def tour_data():
    return {'name': 'test_tour'}

@pytest_asyncio.fixture
async def tour(session, tour_data):
    tour = TourORM(**tour_data)
    session.add(tour)
    await session.commit()
    await session.refresh(tour)
    return tour


@pytest_asyncio.fixture
async def location(session, tour):
    location = LocationORM(name='test_location', tour=tour)
    session.add(location)
    await session.commit()
    await session.refresh(location)
    return location


@pytest_asyncio.fixture
async def list_tours(session):
    tours = [TourORM(name=f'tour_{i}') for i in range(10)]
    session.add_all(tours)
    await session.commit()
    return tours


@pytest_asyncio.fixture
async def list_locations(session):
    locations = [LocationORM(name=f'location_{i}') for i in range(10)]
    session.add_all(locations)
    await session.commit()
    return locations