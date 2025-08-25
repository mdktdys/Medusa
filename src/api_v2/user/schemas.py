from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    role: str | None = None
    photo_base64: str | None = None
