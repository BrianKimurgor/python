from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from app.models.carpark import Carpark

carpark_bp = Blueprint('airport_bp', __name__)

# Add a new carpark (admin only)
@carpark_bp.route('/carparks', methods=['POST'])
@jwt_required()
def add_carpark():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    
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
    return jsonify({"message": "carpark added successfully"}), 201

# Retrieve all carparks
@carpark_bp.route('/carparks', methods=['GET'])
def get_carparks():
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

# Update an carpark by ID (admin only)
@carpark_bp.route('/carparks/<id>', methods=['PUT'])
@jwt_required()
def update_carpark(id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    
    # Find the carpark by ID and update fields
    carpark = Carpark.objects(id=id).first()
    if not carpark:
        return jsonify({"error": "carpark not found"}), 404
    
    carpark.update(**data)  # Update with provided data fields
    return jsonify({"message": "Carpark updated successfully"}), 200

# Delete an carpark by ID (admin only)
@carpark_bp.route('/carparks/<id>', methods=['DELETE'])
@jwt_required()
def delete_carpark(id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    carpark = Carpark.objects(id=id).first()
    if not carpark:
        return jsonify({"error": "Carpark not found"}), 404
    
    carpark.delete()
    return jsonify({"message": "Carpark deleted successfully"}), 200

# Search for carparks by location or facility
@carpark_bp.route('/carparks/search', methods=['GET'])
def search_airports():
    location = request.args.get('location')
    facility = request.args.get('facility')
    query = {}
    
    # Build the query based on location and facility
    if location:
        query['location'] = location
    if facility:
        query['facilities'] = facility
    
    carparks = Carpark.objects(**query)
    return jsonify([{
        'id': str(carpark.id),
        'name': carpark.name,
        'location': carpark.location,
        'totalSpaces': carpark.code,
        'gates': carpark.gates,
        'terminals': carpark.terminals,
        'facilities': carpark.facilities
    } for carpark in carparks]), 200
