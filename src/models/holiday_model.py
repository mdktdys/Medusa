import datetime

from pydantic import BaseModel, ConfigDict


class Holiday(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    id: int
    name: str
    date: datetime.date
        
    @staticmethod
    def fromMap(map: dict) -> "Holiday":
        return Holiday(
            id = map["id"],
            name = map["name"],
            date = datetime.datetime.strptime(map["date"], "%Y-%m-%d").date(),
        )
