import datetime

from pydantic import BaseModel, ConfigDict


class ZamenaFull(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    id: int
    group_id: int
    date: datetime.date
        
    @staticmethod
    def fromMap(map: dict) -> "ZamenaFull":
        return ZamenaFull(
            id = map["id"],
            group_id = map["group"],
            date = datetime.datetime.strptime(map["date"], "%Y-%m-%d").date(),
        )
