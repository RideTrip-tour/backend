from pydantic import BaseModel, ConfigDict


class BaseResultSchema(BaseModel):
    status: str


class BaseModelSchema(BaseModel):
    id: int
    name: str


class ActivitySchema(BaseModelSchema):
    model_config = ConfigDict(from_attributes=True)
    locations: list[BaseModelSchema]


class ActivityListResultSchemas(BaseResultSchema):
    result: list[ActivitySchema] | None


class ActivityItemResultSchema(BaseResultSchema):
    result: ActivitySchema | None


class LocationSchema(BaseModelSchema):
    model_config = ConfigDict(from_attributes=True)
    activities: list[BaseModelSchema]


class LocationListResultSchemas(BaseResultSchema):
    result: list[LocationSchema] | None


class LocationItemResultSchema(BaseResultSchema):
    result: LocationSchema | None
