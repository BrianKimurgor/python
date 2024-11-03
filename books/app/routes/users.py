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
    
    This function retrieves user data from a JSON request, checks if a user with the given
    username already exists, and if not, creates a new user with the specified username and
    password. The password is hashed before being saved. An optional 'admin' flag can be
    included in the request to set the user's admin status.

    Returns:
        Response: A JSON response indicating success or failure of the registration process.
        - On success: {"message": "User registered successfully"}, HTTP status code 201.
        - On failure: {"error": "User already exists"}, HTTP status code 400.
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
    Authenticates a user based on provided JSON credentials and returns an access token if successful.

    Expects a JSON payload with 'username' and 'password' fields.
    If the user exists and the password is correct, an access token is generated and returned.
    If authentication fails, an error message is returned.

    Returns:
        tuple: A JSON response containing either an access token with a 200 status code,
                or an error message with a 401 status code.
    """
    data = request.get_json()
    user = User.objects(username=data['username']).first()
    
    # Check if the user exists and password is correct
    if user and user.check_password(data['password']):
        # Include 'role' in the JWT claims based on admin status
        additional_claims = {"role": "admin"} if user.admin else {"role": "user"}
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"error": "Invalid credentials"}), 401
