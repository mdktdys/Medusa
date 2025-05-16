from supabase import create_client, Client

from my_secrets import SUPABASE_ANON_KEY, SUPABASE_URL

key = SUPABASE_ANON_KEY
url = SUPABASE_URL
supabase_connect: Client = create_client(url, key)
