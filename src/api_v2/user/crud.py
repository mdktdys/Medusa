from src.alchemy.database import User
from .schemas import UserResponse

def me(user: User) -> UserResponse:
    return UserResponse(
        email = user.email,
        first_name = user.first_name,
        last_name = user.last_name,
        username = user.username,
        role = user.role
    )