from flask import Blueprint, request, jsonify
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

share_bp = Blueprint('share', __name__)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@share_bp.route('/add', methods=['POST'])
def share_file():
    data = request.json
    file_id = data.get('file_id')
    recipient_email = data.get('email')
    owner_id = data.get('owner_id')

    try:
        # 1. Find the recipient user's ID using their email
        user_res = supabase.table('users').select("id").eq("email", recipient_email).execute()
        
        if not user_res.data:
            return jsonify({"error": "No user found with that email."}), 404
        
        recipient_id = user_res.data[0]['id']

        # 2. Prevent sharing with yourself
        if str(recipient_id) == str(owner_id):
            return jsonify({"error": "You cannot share a file with yourself."}), 400

        # 3. Create entry in shared_files table using your EXACT column names:
        # Columns: file_id, shared_with_user_id, permission
        supabase.table('shared_files').insert({
            "file_id": file_id,
            "shared_with_user_id": recipient_id,
            "permission": "READ"  # Matches your text column
        }).execute()

        return jsonify({"message": f"Successfully shared with {recipient_email}"}), 200

    except Exception as e:
        # Printing to console helps you see the real error if it fails again
        print(f"Sharing Error: {e}")
        return jsonify({"error": str(e)}), 500