import os

supabase_database_connection = os.environ.get("SUPABASE_DATABASE_CONNECTION")
local_database_connection = os.environ.get("LOCAL_DATABASE_CONNECTION")
SECRET = os.environ.get("SECRET")
API_KEY = os.environ.get("API_KEY")
IS_DEV = os.environ.get("IS_DEV")
BACKEND_URL = os.environ.get("BACKEND_URL")
BROKER_URL = os.environ.get("BROKER_URL")
