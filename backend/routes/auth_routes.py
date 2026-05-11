from flask import Blueprint, request, jsonify
import bcrypt
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

auth_bp = Blueprint('auth', __name__)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Helper: Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Helper: Verify password
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

'''@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    hashed_pw = hash_password(password)

    try:
        # Store in 'users' table
        response = supabase.table('users').insert({
            "name": name,
            "email": email,
            "password": hashed_pw
        }).execute()
        
        return jsonify({"message": "User registered successfully", "user": response.data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        # Fetch user by email
        user_query = supabase.table('users').select("*").eq("email", email).execute()
        
        if not user_query.data:
            return jsonify({"error": "User not found"}), 404

        user = user_query.data[0]
        
        if verify_password(password, user['password']):
            # For simplicity, returning user info as a "session"
            return jsonify({
                "message": "Login successful",
                "user_id": user['id'],
                "email": user['email']
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500'''
# --- UPDATED auth_routes.py ---

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    hashed_pw = hash_password(password)

    try:
        # Use 'password_hash' to match your Supabase column name
        response = supabase.table('users').insert({
            "name": name,
            "email": email,
            "password_hash": hashed_pw 
        }).execute()
        
        return jsonify({"message": "User registered successfully", "user": response.data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        user_query = supabase.table('users').select("*").eq("email", email).execute()
        
        if not user_query.data:
            return jsonify({"error": "User not found"}), 404

        user = user_query.data[0]
        
        # Access 'password_hash' from the database response
        if verify_password(password, user['password_hash']):
            return jsonify({
                "message": "Login successful",
                "user_id": user['id'],
                "email": user['email']
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500