from datetime import time
from pydantic import BaseModel, ConfigDict, Field


class Timing(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    number: int

    start: time
    end: time

    saturday_start: time = Field(alias="saturdayStart")
    saturday_end: time = Field(alias="saturdayEnd")

    obed_start: time = Field(alias="obedStart")
    obed_end: time = Field(alias="obedEnd")