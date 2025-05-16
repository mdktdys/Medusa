from pydantic import BaseModel, ConfigDict
import datetime

class LessonTimings(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    number: int
    start: datetime.time
    end: datetime.time
    saturday_start: datetime.time
    saturday_end: datetime.time
    obed_start: datetime.time
    obed_end: datetime.time
    
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