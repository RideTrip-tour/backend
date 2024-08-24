from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from ...core.tours import schemas
from . import crud

router = APIRouter()


@router.get("/activities", response_model=schemas.ActivityListResultSchemas)
async def get_activities(
    loc: int | None = None, session: AsyncSession = Depends(get_async_session)
):
    activities = await crud.get_list_activities(session, loc=loc)
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
    activity = await crud.get_activity(session, activity_id)
    return {
        "status": "access",
        "result": activity,
    }


@router.get("/locations", response_model=schemas.LocationListResultSchemas)
async def get_locations(
    act: int | None = None, session: AsyncSession = Depends(get_async_session)
):
    locations = await crud.get_list_locations(session, act=act)
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
    location = await crud.get_location(session, location_id)
    return {
        "status": "access",
        "result": location,
    }
