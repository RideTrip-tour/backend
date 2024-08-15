from sqlalchemy import Column, Integer, ForeignKey, String, Table

from src.database import metadata

activity = Table(
    'activities',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String)
)

location = Table(
    'locations',
    metadata,
Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('activity_id', ForeignKey('activities.id')),
)