import os

OPENROUTER_API_KEY: str = os.environ['OPENROUTER_API_KEY']
PUBLIC_API_KEY: str | None = os.environ.get('PUBLIC_API_KEY')
API_KEY: str | None = os.environ.get('API_KEY')
SECRET: str = os.environ['SECRET']
REDIS_PASSWORD: str | None = os.environ.get('REDIS_PASSWORD')

supabase_database_connection: str = os.environ['SUPABASE_DATABASE_CONNECTION']
local_database_connection: str = os.environ['LOCAL_DATABASE_CONNECTION']

SUPABASE_ANON_KEY: str = os.environ['SCHEDULER_SUPABASE_ANON_KEY']
SUPABASE_URL: str = os.environ['SCHEDULER_SUPABASE_URL']

BACKEND_URL: str | None = os.environ.get('BACKEND_URL')
BROKER_URL: str | None = os.environ.get('BROKER_URL')

SCHEDULE_URL = 'https://uksivt.ru/замены'
BASEURL = 'https://www.uksivt.ru/'

FIREBASE_PRIVATE_KEY_ID: str | None = os.environ.get('FIREBASE_PRIVATE_KEY_ID')
FIREBASE_CLIENT_EMAIL: str | None = os.environ.get('FIREBASE_CLIENT_EMAIL')
FIREBASE_PROJECT_ID: str | None = os.environ.get('FIREBASE_PROJECT_ID')
FIREBASE_CLIENT_ID: str | None = os.environ.get('FIREBASE_CLIENT_ID')
FIREBASE_CERT: str | None = os.environ.get('FIREBASE_CERT')

TELEGRAM_API_TOKEN: str | None = os.environ.get('TELEGRAM_API_TOKEN')
TELEGRAM_API_URL: str = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}'
TELEGRAM_DEBUG_CHANNEL: str | None = os.environ.get('TELEGRAM_DEBUG_CHANNEL')

IS_DEV: str | None = os.environ.get('IS_DEV')
