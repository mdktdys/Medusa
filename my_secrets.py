import os

supabase_database_connection = os.environ.get("SUPABASE_DATABASE_CONNECTION")
local_database_connection = os.environ.get("LOCAL_DATABASE_CONNECTION")
SECRET = os.environ.get("SECRET")
API_KEY = os.environ.get("API_KEY")
IS_DEV = os.environ.get("IS_DEV")
BACKEND_URL = os.environ.get("BACKEND_URL")
BROKER_URL = os.environ.get("BROKER_URL")
SCHEDULE_URL = "https://www.uksivt.ru/zameny"
# # SCHEDULE_URL = 'http://127.0.0.1:3000/c:/Users/Danil/Desktop/Uksivt/sample.html'
BASEURL = "https://www.uksivt.ru/"
SUPABASE_URL = os.environ["SCHEDULER_SUPABASE_URL"]
SUPABASE_ANON_KEY = os.environ["SCHEDULER_SUPABASE_ANON_KEY"]
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY")
