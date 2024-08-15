from sqlalchemy import Column, Integer, ForeignKey, String, Table

from src.database import Base

class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)