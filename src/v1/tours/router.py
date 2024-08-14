from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from . import crud, models, schemas

router = APIRouter()


@router.get('/tours/', response_model=schemas.TourListResultSchemas)
async def get_tours(session: AsyncSession = Depends(get_async_session)):
    tours = await crud.get_items(session, models.TourORM)
    return {
        'status': 'access',
        'result': tours.all(),
    }

@router.get('/tours/{tour_id}/', response_model=schemas.TourItemResultSchema)
async def get_tour(tour_id: int, session: AsyncSession = Depends(get_async_session)):
    tour = await crud.get_item(session, models.TourORM, tour_id)
    return {
        'status': 'access',
        'result': tour,
    }

@router.get('/locations/', response_model=schemas.LocationListResultSchemas)
async def get_location(session: AsyncSession = Depends(get_async_session)):
    locations = await crud.get_items(session, models.LocationORM)
    return {
        'status': 'access',
        'result': locations.all(),
    }

