import os

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str = (
        "postgresql+asyncpg://postgres.ojbsikxdqcbuvamygezd:KCQjsy4bJiYqXxL9@aws-0-eu-west-2.pooler.supabase.com:5432/postgres"
    )
    db_echo: bool = True
    app_name: str = "Medusa"
    items_per_user: int = 50


settings = Settings()
