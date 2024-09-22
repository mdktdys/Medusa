import os

from pydantic_settings import BaseSettings
from pathlib import Path

database_connection = os.environ.get("SUPABASE_DATABASE_CONNECTION")
print(database_connection)


class Settings(BaseSettings):
    api_v1_prefix: str = ""
    db_url: str = (
        database_connection
        # f"postgresql+asyncpg://root:{database_pass}@postgres:5432/Devotion"
    )
    db_echo: bool = True
    app_name: str = "Medusa"
    items_per_user: int = 50


settings = Settings()
