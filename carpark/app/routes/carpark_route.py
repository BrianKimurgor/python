from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from app.models.carpark import Carpark

carpark_bp = Blueprint('carpark_bp', __name__)

# Add a new carpark (admin only)
@carpark_bp.route('/carparks', methods=['POST'])
@jwt_required()
def add_carpark():
    """
    Adds a new carpark to the database.

    This function requires the user to have an 'admin' role to execute.
    It retrieves the JSON data from the request, creates a new Carpark
    instance with the provided data, and saves it to the database.

    Returns:
        Response: A JSON response indicating success or failure.
        If the user is not an admin, returns a 403 error with a message.
        If successful, returns a 201 status with a success message.
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()

    try:
        # Create a new carpark instance
        carpark = Carpark(
            name=data['name'],
            location=data['location'],
            totalSpaces=data['totalSpaces'],
            availableSpaces=data['availableSpaces'],
            ratePerHour=data['ratePerHour'],
            facilities=data['facilities']
        )
        carpark.save()  # Save the carpark to the database
        return jsonify({"message": "Carpark added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Retrieve all carparks
@carpark_bp.route('/carparks', methods=['GET'])
def get_carparks():
    """
    Retrieve a list of carparks and return their details in JSON format.

    This function queries the Carpark model to get all carpark objects,
    and then constructs a JSON response containing a list of carparks.
    Each carpark in the list includes the following details:
    - id: The unique identifier of the carpark.
    - name: The name of the carpark.
    - location: The geographical location of the carpark.
    - totalSpaces: The total number of parking spaces available in the carpark.
    - availableSpaces: The number of currently available parking spaces.
    - ratePerHour: The hourly rate for parking in the carpark.
    - facilities: A list of facilities available at the carpark.

    Returns:
        A tuple containing:
        - A JSON response with a list of carpark details.
        - An HTTP status code 200 indicating the request was successful.
    """
    try:
        carparks = Carpark.objects()
        return jsonify([{
            'id': str(carpark.id),
            'name': carpark.name,
            'location': carpark.location,
            'totalSpaces': carpark.totalSpaces,
            'availableSpaces': carpark.availableSpaces,
            'ratePerHour': carpark.ratePerHour,
            'facilities': carpark.facilities
        } for carpark in carparks]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update a carpark by ID (admin only)
@carpark_bp.route('/carparks/<id>', methods=['PUT'])
@jwt_required()
def update_carpark(id):
    """
    Updates the details of a carpark identified by its ID.

    This function requires the user to have an 'admin' role to perform the update.
    It retrieves the JSON data from the request, finds the carpark by the given ID,
    and updates its fields with the provided data.

    Args:
        id (str): The unique identifier of the carpark to be updated.

    Returns:
        Response: A JSON response indicating the result of the update operation.
                - If the user is not an admin, returns a 403 error with a message.
                - If the carpark is not found, returns a 404 error with a message.
                - If the update is successful, returns a 200 status with a success message.
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()

    try:
        # Find the carpark by ID and update fields
        carpark = Carpark.objects(id=id).first()
        if not carpark:
            return jsonify({"error": "Carpark not found"}), 404
        
        carpark.update(**data)  # Update with provided data fields
        return jsonify({"message": "Carpark updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a carpark by ID (admin only)
@carpark_bp.route('/carparks/<id>', methods=['DELETE'])
@jwt_required()
def delete_carpark(id):
    """
    Deletes a carpark with the given ID.

    This function checks if the user has admin access before attempting to delete
    the carpark. If the user is not an admin, it returns a 403 error. If the carpark
    with the specified ID does not exist, it returns a 404 error. Upon successful
    deletion, it returns a success message with a 200 status code.

    Args:
        id: The unique identifier of the carpark to be deleted.

    Returns:
        A JSON response indicating the result of the deletion attempt, along with
        the appropriate HTTP status code.
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    try:
        carpark = Carpark.objects(id=id).first()
        if not carpark:
            return jsonify({"error": "Carpark not found"}), 404
        
        carpark.delete()
        return jsonify({"message": "Carpark deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Search for carparks by location or facility
@carpark_bp.route('/carparks/search', methods=['GET'])
def search_carparks():
    """
    Searches for carparks based on location and facility parameters provided in the request.
    
    Retrieves 'location' and 'facility' from the request arguments and constructs a query
    to filter Carpark objects. Returns a JSON response containing a list of carparks that
    match the query criteria.

    Returns:
        tuple: A JSON response containing a list of carparks with their details and an HTTP status code 200.
    """
    location = request.args.get('location')
    facility = request.args.get('facility')
    query = {}
    
    # Build the query based on location and facility
    if location:
        query['location'] = location
    if facility:
        query['facilities'] = facility

    try:
        carparks = Carpark.objects(**query)
        return jsonify([{
            'id': str(carpark.id),
            'name': carpark.name,
            'location': carpark.location,
            'totalSpaces': carpark.totalSpaces,
            'availableSpaces': carpark.availableSpaces,
            'ratePerHour': carpark.ratePerHour,
            'facilities': carpark.facilities
        } for carpark in carparks]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
