import datetime


class Paras:
    id: int
    group: int
    number: int
    course: int
    teacher: int
    cabinet: int
    date: datetime

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
