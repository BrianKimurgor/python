from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from app.models.user import User

user_bp = Blueprint('user_bp', __name__)

# Register a new user
@user_bp.route('/auth/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    is_admin = data.get('admin', False)
    
    # Check if user already exists
    if User.objects(username=username).first():
        return jsonify({"error": "User already exists"}), 400
    
    # Create a new user
    new_user = User(username=username, admin=is_admin)
    new_user.set_password(password)  # Hash and set the password
    new_user.save()  # Save the user to the database
    
    return jsonify({"message": "User registered successfully"}), 201

# Login endpoint
@user_bp.route('/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.objects(username=data['username']).first()
    
    # Check if the user exists and password is correct
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    
    return jsonify({"error": "Invalid credentials"}), 401
