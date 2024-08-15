from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database import get_async_session
from tests.tours.conftest import activity

from . import  models, schemas

router = APIRouter()


@router.get('/activities/', response_model=schemas.ActivityListResultSchemas)
async def get_activities(session: AsyncSession = Depends(get_async_session)):
    query = models.activity.select()
    response = await session.execute(query)
    activities = response.all()
    return {
        'status': 'access',
        'result': activities,
    }

@router.get('/activities/{activity_id}/', response_model=schemas.ActivityItemResultSchema)
async def get_activity(activity_id: int, session: AsyncSession = Depends(get_async_session)):
    query = models.activity.select().where(models.activity.c.id == activity_id)
    response = await session.execute(query)
    activity = response.first()
    return {
        'status': 'access',
        'result': activity,
    }

@router.get('/locations/',response_model=schemas.LocationListResultSchemas)
async def get_locations(session: AsyncSession = Depends(get_async_session)):
    query = models.location.select()
    response = await session.execute(query)
    locations = response.all()
    return {
        'status': 'access',
        'result': locations,
    }

@router.get('/locations/{location_id}/', response_model=schemas.LocationItemResultSchema)
async def get_location(location_id: int, session: AsyncSession = Depends(get_async_session)):
    query = models.location.select().where(models.location.c.id == location_id)
    response = await session.execute(query)
    location = response.first()
    return {
        'status': 'access',
        'result': location,
    }