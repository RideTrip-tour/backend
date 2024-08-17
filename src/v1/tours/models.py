from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship

from src.database import Base

activities_locations_table = Table(
    "activities_locations",
    Base.metadata,
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
    Column("location_id", ForeignKey("locations.id"), primary_key=True),
)


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    locations: Mapped[list["Location"]] = relationship(
        secondary=activities_locations_table, back_populates="activities"
    )


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    activities: Mapped[list["Activity"]] = relationship(
        secondary=activities_locations_table, back_populates="locations"
    )
