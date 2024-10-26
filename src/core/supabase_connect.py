from supabase import create_client, Client

from my_secrets import SUPABASE_SECRET_KEY, SUPABASE_URL

key = SUPABASE_SECRET_KEY
url = SUPABASE_URL
supabase_connect: Client = create_client(url, key)
