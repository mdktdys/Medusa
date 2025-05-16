import os

PUBLIC_API_KEY = os.environ.get('PUBLIC_API_KEY')
API_KEY = os.environ.get('API_KEY')
SECRET = os.environ.get('SECRET')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

supabase_database_connection: str = os.environ['SUPABASE_DATABASE_CONNECTION']
local_database_connection: str = os.environ['LOCAL_DATABASE_CONNECTION']

SUPABASE_ANON_KEY: str = os.environ['SCHEDULER_SUPABASE_ANON_KEY']
SUPABASE_SECRET_KEY: str = os.environ['SUPABASE_SECRET_KEY']
SUPABASE_URL: str = os.environ['SCHEDULER_SUPABASE_URL']

BACKEND_URL = os.environ.get('BACKEND_URL')
BROKER_URL = os.environ.get('BROKER_URL')

SCHEDULE_URL = 'https://uksivt.ru/замены'
BASEURL = 'https://www.uksivt.ru/'

FIREBASE_PRIVATE_KEY_ID = os.environ.get('FIREBASE_PRIVATE_KEY_ID')
FIREBASE_CLIENT_EMAIL = os.environ.get('FIREBASE_CLIENT_EMAIL')
FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID')
FIREBASE_CLIENT_ID = os.environ.get('FIREBASE_CLIENT_ID')
FIREBASE_CERT = os.environ.get('FIREBASE_CERT')

TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}'

IS_DEV = os.environ.get('IS_DEV')
