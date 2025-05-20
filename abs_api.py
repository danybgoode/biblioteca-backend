import os
import requests

ABS_API_URL = os.getenv("ABS_API_URL")
HEADERS = {"Authorization": f"Bearer {os.getenv('ABS_ADMIN_TOKEN')}"}

def create_abs_user(username, password):
    data = {
        "username": username,
        "password": password,
        "type": "user"
    }
    response = requests.post(f"{ABS_API_URL}/users", json=data, headers=HEADERS)
    return response.json()