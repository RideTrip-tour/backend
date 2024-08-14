from pydantic import BaseModel

class BaseResultSchema(BaseModel):
    status: str

class BaseModelSchema(BaseModel):
    id: int
    name: str


class TourSchema(BaseModelSchema):
    pass

class TourListResultSchemas(BaseResultSchema):
    result: list[TourSchema]

class TourItemResultSchema(BaseResultSchema):
    result: TourSchema | None

class LocationSchema(BaseModelSchema):
    tour: TourSchema


class LocationListResultSchemas(BaseResultSchema):
    result: list[LocationSchema]