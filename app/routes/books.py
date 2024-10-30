from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB setup
client = MongoClient("mongodb://localhost:27017")
db = client["your_database_name"]
books_collection = db["books"]

# Blueprint setup
bp = Blueprint("books", __name__)

# Create a new book
@bp.route("/", methods=["POST"])
def create_book():
    data = request.json
    result = books_collection.insert_one(data)
    return jsonify({"_id": str(result.inserted_id), "message": "Book created successfully"}), 201

# Retrieve all books
@bp.route("/", methods=["GET"])
def get_books():
    books = list(books_collection.find())
    for book in books:
        book["_id"] = str(book["_id"])  # Convert ObjectId to string for JSON serialization
    return jsonify(books), 200

# Retrieve a single book by ID
@bp.route("/<book_id>", methods=["GET"])
def get_book(book_id):
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    if book:
        book["_id"] = str(book["_id"])
        return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

# Update a book by ID
@bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    result = books_collection.update_one({"_id": ObjectId(book_id)}, {"$set": data})
    if result.modified_count:
        return jsonify({"message": "Book updated successfully"}), 200
    return jsonify({"error": "Book not found or no change made"}), 404

# Delete a book by ID
@bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    result = books_collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count:
        return jsonify({"message": "Book deleted successfully"}), 200
    return jsonify({"error": "Book not found"}), 404
