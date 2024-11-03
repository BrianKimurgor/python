from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from app.models.airport import Airport

airport_bp = Blueprint('airport_bp', __name__)

# Add a new airport (admin only)
@airport_bp.route('/airports', methods=['POST'])
@jwt_required()
def add_airport():
    """
    Adds a new airport to the database.

    This function requires the user to have an admin role. It retrieves the
    JSON Web Token (JWT) claims to verify the user's role. If the user is not
    an admin, it returns a 403 error with an appropriate message.

    The function expects a JSON payload with the following fields:
    - name: The name of the airport.
    - location: The location of the airport.
    - code: The airport code.
    - gates: The number of gates at the airport.
    - terminals: The number of terminals at the airport.
    - facilities: The facilities available at the airport.

    If the user is an admin, the function creates a new Airport instance with
    the provided data and saves it to the database. Upon successful addition,
    it returns a success message with a 201 status code.

    Returns:
        Response: A JSON response with a success message and a 201 status code
                  if the airport is added successfully, or an error message
                  with a 403 status code if the user is not an admin.
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    
    # Create a new airport instance
    airport = Airport(
        name=data['name'],
        location=data['location'],
        code=data['code'],
        gates=data['gates'],
        terminals=data['terminals'],
        facilities=data['facilities']
    )
    airport.save()  # Save the airport to the database
    return jsonify({"message": "Airport added successfully"}), 201

# Retrieve all airports
@airport_bp.route('/airports', methods=['GET'])
def get_airports():
    """
    Retrieve a list of airports and return their details in JSON format.

    This function queries the database for all airport objects, extracts relevant
    information from each airport, and returns a JSON response containing a list
    of airports with their details.

    Returns:
        tuple: A tuple containing a JSON response with a list of airports and an HTTP status code 200.
    """
    airports = Airport.objects()
    return jsonify([{
        'id': str(airport.id),
        'name': airport.name,
        'location': airport.location,
        'code': airport.code,
        'gates': airport.gates,
        'terminals': airport.terminals,
        'facilities': airport.facilities
    } for airport in airports]), 200

# Update an airport by ID (admin only)
@airport_bp.route('/airports/<id>', methods=['PUT'])
@jwt_required()
def update_airport(id):
    """
    Update an airport's information based on the provided ID.

    This function requires the user to have an admin role to perform the update.
    It retrieves the JSON data from the request, finds the airport by the given ID,
    and updates the airport's fields with the provided data.

    Args:
        id (str): The unique identifier of the airport to be updated.

    Returns:
        Response: A JSON response indicating the result of the update operation.
                - If the user is not an admin, returns a 403 error with a message.
                - If the airport is not found, returns a 404 error with a message.
                - If the update is successful, returns a 200 status with a success message.
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    
    # Find the airport by ID and update fields
    airport = Airport.objects(id=id).first()
    if not airport:
        return jsonify({"error": "Airport not found"}), 404
    
    airport.update(**data)  # Update with provided data fields
    return jsonify({"message": "Airport updated successfully"}), 200

# Delete an airport by ID (admin only)
@airport_bp.route('/airports/<id>', methods=['DELETE'])
@jwt_required()
def delete_airport(id):
    """
    Deletes an airport from the database based on the provided airport ID.
    
    This function first checks if the user has admin privileges by inspecting the [JWT](https://jwt.io/) claims.
    If the user is not an admin, it returns a 403 error. If the airport with the given ID
    does not exist, it returns a 404 error. If the airport is found and the user is an admin,
    it deletes the airport and returns a success message with a 200 status code.

    Args:
        id (str): The unique identifier of the airport to be deleted.

    Returns:
        Response: A [JSON](https://www.json.org/json-en.html) response with a success message and a 200 status code if the airport
                is deleted successfully, or an error message with a 403 or 404 status code
                if the operation fails.
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    airport = Airport.objects(id=id).first()
    if not airport:
        return jsonify({"error": "Airport not found"}), 404
    
    airport.delete()
    return jsonify({"message": "Airport deleted successfully"}), 200

# Search for airports by location or facility
@airport_bp.route('/airports/search', methods=['GET'])
def search_airports():
    """
    Searches for airports based on location and facility criteria provided in the request arguments.
    
    Retrieves 'location' and 'facility' from the request arguments and constructs a query to filter airports.
    Returns a JSON response containing a list of airports that match the query criteria.
    
    Returns:
        tuple: A JSON response with a list of airports and an HTTP status code 200.
    """
    location = request.args.get('location')
    facility = request.args.get('facility')
    query = {}
    
    # Build the query based on location and facility
    if location:
        query['location'] = location
    if facility:
        query['facilities'] = facility
    
    airports = Airport.objects(**query)
    return jsonify([{
        'id': str(airport.id),
        'name': airport.name,
        'location': airport.location,
        'code': airport.code,
        'gates': airport.gates,
        'terminals': airport.terminals,
        'facilities': airport.facilities
    } for airport in airports]), 200
