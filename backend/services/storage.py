from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_file(bucket_name, path, file_bytes):
    """
    Uploads bytes to a specific Supabase bucket path.
    path should be: user_id/category/filename
    """
    try:
        # We use upsert=True so that if you upload the same file twice, 
        # it updates instead of throwing an error.
        response = supabase.storage.from_(bucket_name).upload(
            path=path,
            file=file_bytes,
            file_options={
                "content-type": "application/octet-stream",
                "x-upsert": "true" 
            }
        )
        
        # Check if the response contains an error (for some client versions)
        if hasattr(response, 'error') and response.error is not None:
            print(f"Supabase Storage Error: {response.error}")
            return None
            
        return response
    except Exception as e:
        print(f"Critical Upload Error in storage.py: {e}")
        return None

def download_file(bucket_name, path):
    """
    Downloads bytes from a specific Supabase bucket path.
    """
    try:
        response = supabase.storage.from_(bucket_name).download(path)
        return response
    except Exception as e:
        print(f"Download Error in storage.py: {e}")
        return None