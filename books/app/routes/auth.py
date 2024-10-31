from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = register_user(data['username'], data['password'], data.get('admin', False))
    return jsonify({"message": "User registered successfully", "user": user.username}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    token = login_user(data['username'], data['password'])
    if token:
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401
