from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from scr.database import Base


class TourORM(Base):
    __tablename__ = 'tours'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    locations = relationship('LocationORM', back_populates='tour')


class LocationORM(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    tour_id = Column(ForeignKey('tours.id'))
    tour = relationship(TourORM, back_populates='locations')
