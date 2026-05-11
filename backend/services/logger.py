from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def log_activity(user_id, action, details=""):
    try:
        supabase.table('activity_logs').insert({
            "user_id": user_id,
            "action": action,
            "details": details 
            # 'timestamp' and 'id' are handled automatically by Supabase
        }).execute()
    except Exception as e:
        print(f"Logging failed: {e}")