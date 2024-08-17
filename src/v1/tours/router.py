from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database import get_async_session

from . import models, schemas

router = APIRouter()


@router.get("/activities", response_model=schemas.ActivityListResultSchemas)
async def get_activities(
    loc: int | None = None, session: AsyncSession = Depends(get_async_session)
):
    query = select(models.Activity).options(
        joinedload(models.Activity.locations)
    )
    if loc:
        query = query.where(
            models.Activity.locations.any(models.Location.id == loc)
        )
    response = await session.execute(query)
    activities = response.scalars().unique()
    return {
        "status": "access",
        "result": activities,
    }


@router.get(
    "/activities/{activity_id}",
    response_model=schemas.ActivityItemResultSchema,
)
async def get_activity(
    activity_id: int, session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(models.Activity)
        .options(joinedload(models.Activity.locations))
        .filter_by(id=activity_id)
    )
    response = await session.execute(query)
    activity = response.scalar()
    return {
        "status": "access",
        "result": activity,
    }


@router.get("/locations", response_model=schemas.LocationListResultSchemas)
async def get_locations(
    act: int | None = None, session: AsyncSession = Depends(get_async_session)
):
    query = select(models.Location).options(
        joinedload(models.Location.activities)
    )
    if act:
        query = query.where(
            models.Location.activities.any(models.Activity.id == act)
        )
    response = await session.execute(query)
    locations = response.scalars().unique()
    return {
        "status": "access",
        "result": locations,
    }


@router.get(
    "/locations/{location_id}", response_model=schemas.LocationItemResultSchema
)
async def get_location(
    location_id: int, session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(models.Location)
        .options(joinedload(models.Location.activities))
        .filter_by(id=location_id)
    )
    response = await session.execute(query)
    location = response.scalar()
    return {
        "status": "access",
        "result": location,
    }
