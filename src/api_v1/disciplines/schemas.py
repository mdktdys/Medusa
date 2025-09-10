from pydantic import BaseModel


class CreateDisciplineAliasRequest(BaseModel):
    discipline_id: int
    alias: str