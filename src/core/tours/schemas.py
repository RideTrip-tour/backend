from pydantic import BaseModel, ConfigDict


class BaseResultSchema(BaseModel):
    status: str


class BaseModelSchema(BaseModel):
    id: int
    name: str


class CountrySchema(BaseModelSchema):
    model_config = ConfigDict(from_attributes=True)


class LocationSchema(BaseModelSchema):
    model_config = ConfigDict(from_attributes=True)
    country: CountrySchema


class ActivitySchema(BaseModelSchema):
    model_config = ConfigDict(from_attributes=True)
    locations: list[LocationSchema]


class ActivityListResultSchemas(BaseResultSchema):
    result: list[ActivitySchema] | None


class ActivityItemResultSchema(BaseResultSchema):
    result: ActivitySchema | None


class LocationSchemaWithActivities(BaseModelSchema):
    model_config = ConfigDict(from_attributes=True)
    country: CountrySchema
    activities: list[BaseModelSchema]


class LocationListResultSchemas(BaseResultSchema):
    result: list[LocationSchemaWithActivities] | None


class LocationItemResultSchema(BaseResultSchema):
    result: LocationSchemaWithActivities | None
