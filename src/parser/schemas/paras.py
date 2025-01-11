from pydantic import BaseModel, ConfigDict


class Paras(BaseModel):
    model_config = ConfigDict()
    group: int
    number: int
    course: int
    teacher: int
    cabinet: int
    date: str
