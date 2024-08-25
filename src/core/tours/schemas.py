from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BaseResultSchema(BaseModel):
    status: str


class IDFieldModelSchema(BaseModel):
    id: int


class NameFieldModelSchema(IDFieldModelSchema):
    name: str


class CountrySchema(NameFieldModelSchema):
    model_config = ConfigDict(from_attributes=True)


class LocationSchema(NameFieldModelSchema):
    model_config = ConfigDict(from_attributes=True)
    country: CountrySchema


class ActivitySchema(NameFieldModelSchema):
    model_config = ConfigDict(from_attributes=True)


class ActivitySchemaWithLocations(NameFieldModelSchema):
    model_config = ConfigDict(from_attributes=True)
    locations: list[LocationSchema]


class ActivityListResultSchema(BaseResultSchema):
    result: list[ActivitySchemaWithLocations] | None


class ActivityItemResultSchema(BaseResultSchema):
    result: ActivitySchemaWithLocations | None


class LocationSchemaWithActivities(NameFieldModelSchema):
    model_config = ConfigDict(from_attributes=True)
    country: CountrySchema
    activities: list[ActivitySchema]


class LocationListResultSchema(BaseResultSchema):
    result: list[LocationSchemaWithActivities] | None


class LocationItemResultSchema(BaseResultSchema):
    result: LocationSchemaWithActivities | None


class TransportTypeSchema(NameFieldModelSchema):
    model_config = ConfigDict(from_attributes=True)


class TripSegmentSchema(IDFieldModelSchema):
    model_config = ConfigDict(from_attributes=True)
    transport_type: TransportTypeSchema
    created_at: datetime
    start_at: datetime
    finish_at: datetime
    price: Decimal
    start_location: LocationSchema
    target_location: LocationSchema


class TripSchema(IDFieldModelSchema):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    start_at: datetime
    finish_at: datetime
    start_location: LocationSchema
    target_location: LocationSchema
    segments: list[TripSegmentSchema]


class AccommodationTypeSchema(NameFieldModelSchema):
    model_config = ConfigDict(from_attributes=True)


class AccommodationSchema(IDFieldModelSchema):
    model_config = ConfigDict(from_attributes=True)
    accommodation_type: AccommodationTypeSchema
    created_at: datetime
    checkin_at: datetime
    checkout_at: datetime
    location: LocationSchema
    price: Decimal


class TourSchema(IDFieldModelSchema):
    model_config = ConfigDict(from_attributes=True)
    description: str
    activity: ActivitySchema
    target_location: LocationSchema
    start_location: LocationSchema
    departure_trip: TripSchema
    return_trip: TripSchema
    accommodation: AccommodationSchema


class TourListResultSchema(BaseResultSchema):
    result: list[TourSchema]
