from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_async_session

from . import  models, schemas

router = APIRouter()


@router.get('/activities', response_model=schemas.ActivityListResultSchemas)
async def get_activities(session: AsyncSession = Depends(get_async_session)):
    query = select(models.Activity)
    activities = await session.scalars(query)
    return {
        'status': 'access',
        'result': activities,
    }

@router.get('/activities/{activity_id}/', response_model=schemas.ActivityItemResultSchema)
async def get_activity(activity_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(models.Activity).filter_by(id=activity_id)
    activity = await session.scalar(query)
    return {
        'status': 'access',
        'result': activity,
    }

@router.get('/locations',response_model=schemas.LocationListResultSchemas)
async def get_locations(session: AsyncSession = Depends(get_async_session)):
    query = select(models.Location)
    locations = await session.scalars(query)
    return {
        'status': 'access',
        'result': locations,
    }

@router.get('/locations/{location_id}/', response_model=schemas.LocationItemResultSchema)
async def get_location(location_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(models.Location).filter_by(id=location_id)
    location = await session.scalar(query)
    return {
        'status': 'access',
        'result': location,
    }