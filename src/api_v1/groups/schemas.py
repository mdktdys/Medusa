from pydantic import BaseModel, ConfigDict


class GroupBase(BaseModel):
    id: int


class GroupGet:
    pass


class Group(GroupBase):
    model_config = ConfigDict(from_attributes=True)
    name: str
    department: int
