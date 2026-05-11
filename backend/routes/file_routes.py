from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
from services.encryption import encrypt_file, decrypt_file
from services.storage import upload_file, download_file
from services.logger import log_activity 
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

file_bp = Blueprint('file', __name__)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 1. UPLOAD ROUTE ---
@file_bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    user_id = request.form.get('user_id')
    category = request.form.get('category') 
    filename = file.filename

    if not user_id or not category:
        return jsonify({"error": "Missing user_id or category"}), 400

    try:
        # Encrypt the file content
        file_bytes = file.read()
        encrypted_data = encrypt_file(file_bytes)

        # Define path: user_id/category/filename
        storage_path = f"{user_id}/{category}/{filename}"

        # Upload to Supabase Storage
        upload_res = upload_file("student-files", storage_path, encrypted_data)

        if upload_res:
            # Store metadata in 'files' table
            supabase.table('files').insert({
                "user_id": user_id,
                "file_name": filename,
                "category": category,
                "storage_path": storage_path
            }).execute()

            # Log the activity
            log_activity(user_id, "UPLOAD", f"Uploaded: {filename} ({category})")

            return jsonify({"message": "File encrypted and uploaded successfully"}), 200
        else:
            return jsonify({"error": "Storage upload failed"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- 2. DOWNLOAD ROUTE ---
@file_bp.route('/download/<file_id>', methods=['GET'])
def download(file_id):
    user_id = request.args.get('user_id') 

    if not user_id:
        return jsonify({"error": "User ID required for verification"}), 400

    try:
        # Fetch metadata
        file_res = supabase.table('files').select("*").eq("id", file_id).execute()
        
        if not file_res.data:
            return jsonify({"error": "File record not found"}), 404
        
        file_metadata = file_res.data[0]

        # Security Check: In a real app, check if user_id is owner OR has share record
        # For now, we allow the owner. 
        # (Extension: Add logic here to check 'shared_files' table too)

        # Download encrypted bytes from Supabase
        encrypted_bytes = download_file("student-files", file_metadata['storage_path'])
        
        if not encrypted_bytes:
            return jsonify({"error": "File could not be retrieved from storage"}), 500

        # Decrypt
        decrypted_data = decrypt_file(encrypted_bytes)

        # Log Activity
        log_activity(user_id, "DOWNLOAD", f"Downloaded: {file_metadata['file_name']}")

        return send_file(
            BytesIO(decrypted_data),
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name=file_metadata['file_name']
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- 3. LIST OWNED FILES ROUTE ---
@file_bp.route('/list/<user_id>', methods=['GET'])
def list_files(user_id):
    try:
        # Uses your specific 'upload_time' column for sorting
        res = supabase.table('files').select("*").eq("user_id", user_id).order("upload_time", desc=True).execute()
        return jsonify(res.data), 200
    except Exception as e:
        print(f"List Error: {e}")
        return jsonify({"error": str(e)}), 500


# --- 4. LIST SHARED FILES ROUTE ---
@file_bp.route('/shared/<user_id>', methods=['GET'])
def list_shared_files(user_id):
    try:
        # Step 1: Find file IDs shared with this user
        shared_ref = supabase.table('shared_files')\
            .select("file_id")\
            .eq("shared_with_user_id", user_id)\
            .execute()
        
        if not shared_ref.data:
            return jsonify([]), 200

        file_ids = [item['file_id'] for item in shared_ref.data]

        # Step 2: Fetch the actual file details for those IDs
        files_res = supabase.table('files')\
            .select("*")\
            .in_("id", file_ids)\
            .execute()
            
        return jsonify(files_res.data), 200
    except Exception as e:
        print(f"Shared Fetch Error: {e}")
        return jsonify({"error": str(e)}), 500