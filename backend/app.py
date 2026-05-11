from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.file_routes import file_bp
from config import DEBUG
from routes.share_routes import share_bp
from flask import Flask, jsonify

app = Flask(__name__)
CORS(app) # Allows your Streamlit frontend to talk to this API

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(file_bp, url_prefix='/files')
app.register_blueprint(share_bp, url_prefix='/share')

@app.route('/')
def health_check():
    return {"status": "Backend is running"}, 200

if __name__ == '__main__':
    app.run(debug=DEBUG, port=5000)

@app.route('/logs/<user_id>', methods=['GET'])
def get_logs(user_id):
    try:
        # Fetching logs using your 'timestamp' column name
        response = supabase.table('activity_logs')\
            .select("*")\
            .eq("user_id", user_id)\
            .order("timestamp", desc=True)\
            .limit(10)\
            .execute()
        
        return jsonify(response.data), 200
    except Exception as e:
        print(f"Log Fetch Error: {e}")
        return jsonify({"error": str(e)}), 500