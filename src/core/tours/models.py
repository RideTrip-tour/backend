from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
)
from sqlalchemy.orm import Mapped, relationship

from src.database import Base

activities_locations_table = Table(
    "activities_locations",
    Base.metadata,
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
    Column("location_id", ForeignKey("locations.id"), primary_key=True),
)

trips_segments_table = Table(
    "trips_segments",
    Base.metadata,
    Column(
        "trip_segment_id", ForeignKey("trip_segments.id"), primary_key=True
    ),
    Column("trip_id", ForeignKey("trips.id"), primary_key=True),
)


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    locations: Mapped[list["Location"]] = relationship(
        secondary=activities_locations_table, back_populates="activities"
    )


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def __str__(self):
        return self.name


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    activities: Mapped[list["Activity"]] = relationship(
        secondary=activities_locations_table, back_populates="locations"
    )
    country_id = Column(ForeignKey("countries.id"), nullable=False)
    country: Mapped["Country"] = relationship()


class TransportType(Base):
    __tablename__ = "transport_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class TripSegment(Base):
    __tablename__ = "trip_segments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_transport_id = Column(
        ForeignKey("transport_types.id"), nullable=False
    )
    type_transport: Mapped["TransportType"] = relationship()
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
    start_at = Column(
        DateTime,
        nullable=False,
    )
    finish_at = Column(
        DateTime,
        nullable=False,
    )
    prise = Column(Numeric(10, 2), nullable=False)
    start_location_id = Column(ForeignKey("locations.id"), nullable=False)
    start_location: Mapped["Location"] = relationship(
        foreign_keys=[start_location_id]
    )
    target_location_id = Column(ForeignKey("locations.id"), nullable=False)
    target_location: Mapped["Location"] = relationship(
        foreign_keys=[target_location_id]
    )
    trips: Mapped[list["Trip"]] = relationship(
        secondary=trips_segments_table, back_populates="segments"
    )


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, autoincrement=True)
    segments: Mapped[list["TripSegment"]] = relationship(
        secondary=trips_segments_table, back_populates="trips"
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
    start_at = Column(
        DateTime,
        nullable=False,
    )
    finish_at = Column(
        DateTime,
        nullable=False,
    )
    start_location_id = Column(ForeignKey("locations.id"), nullable=False)
    start_location: Mapped["Location"] = relationship(
        foreign_keys=[start_location_id]
    )
    target_location_id = Column(ForeignKey("locations.id"), nullable=False)
    target_location: Mapped["Location"] = relationship(
        foreign_keys=[target_location_id]
    )
    activity_id = Column(ForeignKey("activities.id"), nullable=False)
    activity: Mapped["Activity"] = relationship()
