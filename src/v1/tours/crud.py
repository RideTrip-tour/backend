from sqlalchemy import Result, ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ...core.tours import models


async def get_list_locations(
    session: AsyncSession, act: int | None = None
) -> ScalarResult:
    """
    Возвращает список локаций
    :param session:
        Сессия
    :param act:
        Если указан, выбирает только те локации,
        которые содержат активность с этим id
    :return:
        Список локаций
    """
    query = select(
        models.Location,
    ).options(
        joinedload(models.Location.activities),
        joinedload(models.Location.country),
    )
    if act:
        query = query.where(
            models.Location.activities.any(models.Activity.id == act)
        )
    response = await session.execute(query)
    return response.scalars().unique()


async def get_list_activities(
    session: AsyncSession, loc: int | None = None
) -> ScalarResult:
    """
    Возвращает список активностей
    :param session:
        Сессия
    :param loc:
        Если указан, выбирает только те активности,
        которые содержат локацию с этим id
    :return:
        Список активностей
    """
    query = select(models.Activity).options(
        joinedload(models.Activity.locations).joinedload(
            models.Location.country
        )
    )
    if loc:
        query = query.where(
            models.Activity.locations.any(models.Location.id == loc)
        )
    response = await session.execute(query)
    return response.scalars().unique()


async def get_activity(
    session: AsyncSession, activity_id: int
) -> Result | None:
    """
    Возвращает активность по ID
    :param session:
        Сессия
    :param activity_id:
        ID нужной активности
    :return:
        Активность
    """
    query = (
        select(models.Activity)
        .options(
            joinedload(models.Activity.locations).joinedload(
                models.Location.country
            )
        )
        .filter_by(id=activity_id)
    )
    response = await session.execute(query)
    return response.scalar()


async def get_location(
    session: AsyncSession, location_id: int
) -> Result | None:
    """
    Возвращает локацию по ID
    :param session:
        Сессия
    :param location_id:
        ID нужной локации
    :return:
        Локацию
    """
    query = (
        select(models.Location)
        .options(
            joinedload(models.Location.activities),
            joinedload(models.Location.country),
        )
        .filter_by(id=location_id)
    )
    response = await session.execute(query)
    return response.scalar()
