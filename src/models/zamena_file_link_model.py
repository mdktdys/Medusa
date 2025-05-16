import datetime


class ZamenaFileLink:
    id: int
    link: str
    date: datetime.date
    created_at: datetime.datetime
    hash: str

    def __init__(
        self,
        id: int,
        link: str,
        date: datetime.date,
        created_at: datetime.datetime,
        hash: str
    ):
        self.id = id
        self.link = link
        self.date = date
        self.created_at = created_at
        self.hash = hash
        
    @staticmethod
    def fromMap(map: dict) -> "ZamenaFileLink":
        return ZamenaFileLink(
            id = map["id"],
            link = map["link"],
            date = datetime.datetime.strptime(map["date"], "%Y-%m-%d").date(),
            created_at = datetime.datetime.strptime(map["date"], "%Y-%m-%d"),
            hash = map["hash"],
        )
