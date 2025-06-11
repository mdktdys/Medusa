from pydantic import BaseModel, ConfigDict


class Course(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    fullname: str
    synonyms: list[str]