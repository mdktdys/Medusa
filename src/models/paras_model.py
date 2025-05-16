import datetime


class Paras:
    id: int
    group: int
    number: int
    course: int
    teacher: int
    cabinet: int
    date: datetime.date

    def __init__(
        self,
        id: int,
        group: int,
        number: int,
        course: int,
        teacher: int,
        cabinet: int,
        date: datetime.date,
    ):
        self.id = id
        self.group = group
        self.number = number
        self.course = course
        self.teacher = teacher
        self.cabinet = cabinet
        self.date = date

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
    def fromMap(map: dict) -> "Paras":
        return Paras(
            id=map["id"],
            group=map["group"],
            number=map["number"],
            course=map["course"],
            teacher=map["teacher"],
            cabinet=map["cabinet"],
            date=datetime.datetime.strptime(map["date"], "%Y-%m-%d").date()
        )
        
