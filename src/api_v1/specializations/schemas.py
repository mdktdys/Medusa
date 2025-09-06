from pydantic import BaseModel


class SpecializationDto(BaseModel):
    id: int
    name: str
    code: str


class SpecializationsResponse(BaseModel):
    specialization: list[SpecializationDto]
