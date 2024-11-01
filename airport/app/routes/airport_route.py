from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from app.models.airport import Airport

airport_bp = Blueprint('airport_bp', __name__)

# Add a new airport (admin only)
@airport_bp.route('/airports', methods=['POST'])
@jwt_required()
def add_airport():
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
