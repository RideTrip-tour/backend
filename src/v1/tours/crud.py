from sqlalchemy import select

from src.database import Base


async def get_items(session, model: Base):
    query = select(model)
    result = await session.execute(query)
    return result.scalars()

async def get_item(session, model: Base, item_id):
    query = select(model).where(model.id == item_id)
    item = await session.execute(query)
    return item.scalar_one_or_none()

