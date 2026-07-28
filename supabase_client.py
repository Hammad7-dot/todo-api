import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Missing SUPABASE_URL or SUPABASE_KEY. Did you create a .env file from .env.example?"
    )

# NEVER use the service_role key here — only the anon (public) key.
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
