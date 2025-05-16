import datetime


class Holiday:
    id: int
    name: str
    date: datetime.date

    def __init__(
        self,
        id: int,
        name: str,
        date: datetime.date,
    ):
        self.id = id
        self.name = name
        self.date = date
        
    @staticmethod
    def fromMap(map: dict) -> "Holiday":
        return Holiday(
            id = map["id"],
            name = map["name"],
            date = datetime.datetime.strptime(map["date"], "%Y-%m-%d").date(),
        )
