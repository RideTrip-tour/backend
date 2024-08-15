from pydantic import BaseModel

class BaseResultSchema(BaseModel):
    status: str

class BaseModelSchema(BaseModel):
    id: int
    name: str


class ActivitySchema(BaseModelSchema):
    pass


class ActivityListResultSchemas(BaseResultSchema):
    result: list[ActivitySchema]

class ActivityItemResultSchema(BaseResultSchema):
    result: ActivitySchema | None

class LocationSchema(BaseModelSchema):
    activity_id: int
    activity_name: str



class LocationListResultSchemas(BaseResultSchema):
    result: list[LocationSchema]