import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User
from abs_api import create_abs_user
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://bibliotecanocturna.com.mx"])

# SQLite DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    email = data.get("email")
    password = data.get("password")
    plan = data.get("plan", "freemium")  # ✅ FIX: define plan with a default

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    hashed_password = generate_password_hash(password)

    abs_url = os.environ.get("ABS_API_URL")
    abs_token = os.environ.get("ABS_ADMIN_TOKEN")

    headers = {
        "Authorization": f"Bearer {abs_token}",
        "Content-Type": "application/json"
    }

    abs_payload = {
        "username": email,
        "email": email,
        "password": password,
        "type": "user",
        "isActive": True,
        "permissions": {
            "download": False,
            "update": False,
            "delete": False,
            "upload": False,
            "accessAllLibraries": True,
            "accessAllTags": True,
            "accessExplicitContent": True
        }
    }

    try:
        abs_response = requests.post(f"{abs_url}/users", headers=headers, json=abs_payload)
        print("ABS Response:", abs_response.status_code, abs_response.text)

        if abs_response.status_code == 200:
            abs_data = abs_response.json()
            abs_user_id = abs_data.get("user", {}).get("id")

            # Save user in local DB
            new_user = User(email=email, password=hashed_password, abs_user_id=abs_user_id, plan=plan)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"message": "User created successfully"})
        else:
            return jsonify({"error": "ABS user creation failed", "details": abs_response.text}), abs_response.status_code
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"error": "Exception occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5433)  # or change port as needed