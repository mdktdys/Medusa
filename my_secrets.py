import os
print(os.environ.keys())
supabase_database_connection = os.environ.get("SUPABASE_DATABASE_CONNECTION")
local_database_connection = os.environ.get("LOCAL_DATABASE_CONNECTION")
SECRET = os.environ.get("SECRET")
API_KEY = os.environ.get("API_KEY")
PUBLIC_API_KEY = os.environ.get("PUBLIC_API_KEY")
IS_DEV = os.environ.get("IS_DEV")
BACKEND_URL = os.environ.get("BACKEND_URL")
BROKER_URL = os.environ.get("BROKER_URL")

TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}"

SCHEDULE_URL = "https://www.uksivt.ru/замены"
# # SCHEDULE_URL = 'http://127.0.0.1:3000/c:/Users/Danil/Desktop/Uksivt/sample.html'
BASEURL = "https://www.uksivt.ru/"

SUPABASE_URL = os.environ["SCHEDULER_SUPABASE_URL"]
SUPABASE_ANON_KEY = os.environ["SCHEDULER_SUPABASE_ANON_KEY"]
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY")

FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID")
FIREBASE_PRIVATE_KEY_ID = os.environ.get("FIREBASE_PRIVATE_KEY_ID")
FIREBASE_PRIVATE_KEY = os.environ.get("FIREBASE_PRIVATE_KEY")
FIREBASE_CLIENT_ID = os.environ.get("FIREBASE_CLIENT_ID")
FIREBASE_CLIENT_EMAIL = os.environ.get("FIREBASE_CLIENT_EMAIL")
FIREBASE_CERT = os.environ.get("FIREBASE_CERT")
