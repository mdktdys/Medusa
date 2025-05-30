import datetime

from pydantic import BaseModel, ConfigDict


class Zamenas(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    id: int
    group: int
    number: int
    course: int
    teacher: int
    cabinet: int
    date: datetime.date

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "group": self.group,
            "number": self.number,
            "course": self.course,
            "teacher": self.teacher,
            "cabinet": self.cabinet,
            "date": self.date.strftime("%Y-%m-%d"),
        }
        
    @staticmethod
    def fromMap(map: dict) -> "Zamenas":
        return Zamenas(
            id=map["id"],
            group=map["group"],
            number=map["number"],
            course=map["course"],
            teacher=map["teacher"],
            cabinet=map["cabinet"],
            date=datetime.datetime.strptime(map["date"], "%Y-%m-%d").date()
        )
