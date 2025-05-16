import datetime

from pydantic import BaseModel, ConfigDict


class ZamenaFileLink(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    id: int
    link: str
    date: datetime.date
    created_at: datetime.datetime
    hash: str
        
    @staticmethod
    def fromMap(map: dict) -> "ZamenaFileLink":
        return ZamenaFileLink(
            id = map["id"],
            link = map["link"],
            date = datetime.datetime.strptime(map["date"], "%Y-%m-%d").date(),
            created_at = datetime.datetime.strptime(map["date"], "%Y-%m-%d"),
            hash = map["hash"],
        )
