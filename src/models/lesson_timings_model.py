from pydantic import BaseModel, ConfigDict
import datetime

class LessonTimings(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    number: int
    start: datetime.datetime
    end: datetime.datetime
    saturday_start: datetime.datetime
    saturday_end: datetime.datetime
    obed_start: datetime.datetime
    obed_end: datetime.datetime
    
    @staticmethod
    def fromMap(data: dict) -> "LessonTimings":
        return LessonTimings(
            number = data['number'],
            start = data['start'],
            end = data['end'],
            saturday_start = data['saturdayStart'],
            saturday_end = data['saturdayEnd'],
            obed_start = data['obedStart'],
            obed_end = data['obedEnd'],
        )