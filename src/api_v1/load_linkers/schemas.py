from pydantic import BaseModel


class LoadLinkersRequest(BaseModel):
    group_id: int
    