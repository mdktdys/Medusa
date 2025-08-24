from pydantic import BaseModel


class SearchItemDto(BaseModel):
    uid: str
    name: str

    class Config:
        orm_mode = True