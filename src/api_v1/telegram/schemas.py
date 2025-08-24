from typing import Optional

from pydantic import BaseModel, ConfigDict


class Subscription(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    chat_id: str
    target_type: int
    target_id: int


class DaySchedule(BaseModel):
    model_config = ConfigDict(from_attributes=True)
        model_config = ConfigDict(from_attributes=True)
    