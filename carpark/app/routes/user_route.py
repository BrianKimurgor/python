from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from app.models.user import User

user_bp = Blueprint('user_bp', __name__)

# Register a new user
@user_bp.route('/auth/register', methods=['POST'])
def register_user():
    """
    Registers a new user with the provided username and password.
    
    Expects a JSON payload with the following structure:
    {
        "username": "desired_username",
        "password": "desired_password",
        "admin": false  # Optional, defaults to False
    }
    
    Returns:
        A JSON response indicating success or failure:
        - On success: {"message": "User registered successfully"}, HTTP status 201
        - On failure: {"error": "User already exists"}, HTTP status 400
    """
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
    """
    Authenticates a user based on the provided username and password.

    Retrieves JSON data from the request, checks if a user with the given
    username exists, and verifies the password. If authentication is successful,
    an access token is generated and returned. Otherwise, an error message is returned.

    Returns:
        tuple: A JSON response containing the access token and a status code of 200
            if authentication is successful, or an error message and a status code
            of 401 if authentication fails.
    """
    data = request.get_json()
    user = User.objects(username=data['username']).first()
    
    # Check if the user exists and password is correct
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    
    return jsonify({"error": "Invalid credentials"}), 401
