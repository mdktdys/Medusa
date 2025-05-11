from pydantic import BaseModel, ConfigDict

class FirebaseSubscriber(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    client_id: int
    token: str


class FirebaseMessage(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    body: str