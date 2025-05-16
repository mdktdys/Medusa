import datetime


class ZamenaFull:
    id: int
    group_id: int
    date: datetime.date

    def __init__(
        self,
        id: int,
        group_id: int,
        date: datetime.date,
    ):
        self.id = id
        self.date = date
        self.group_id = group_id
        
    @staticmethod
    def fromMap(map: dict) -> "ZamenaFull":
        return ZamenaFull(
            id = map["id"],
            group_id = map["group"],
            date = datetime.datetime.strptime(map["date"], "%Y-%m-%d").date(),
        )
