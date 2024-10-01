from pydantic_settings import BaseSettings

from secrets import supabase_database_connection, local_database_connection


class Settings(BaseSettings):
    db_url: str = supabase_database_connection
    local_db: str = local_database_connection
    db_echo: bool = False
    app_name: str = "Medusa"
    items_per_user: int = 50


settings = Settings()
