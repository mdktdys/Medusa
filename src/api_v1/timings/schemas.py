from datetime import time
from pydantic import BaseModel, ConfigDict


class Timing(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    number: int
    
    start: time
    end: time
    
    saturday_start: time
    saturday_end: time

    obed_start: time
    obed_end: time