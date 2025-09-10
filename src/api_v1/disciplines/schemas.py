from pydantic import BaseModel


class CreateDisciplineAliasRequest(BaseModel):
    discipline_id: int
    alias: str
    
    
class DisciplineAliasesRequest(BaseModel):
    discipline_id: int
    
    
class DeleteDisciplineAliasesRequest(BaseModel):
    alias_id: int