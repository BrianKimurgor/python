from flask import Blueprint, request, jsonify
from services.book_service import create_book, get_books, update_book, delete_book

from flask_jwt_extended import jwt_required


books = Blueprint('books', __name__)

@books.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    book = create_book(data)
    return jsonify({"message": "Book added", "book": book.title}), 201

@books.route('/books', methods=['GET'])
def list_books():
    books = get_books()
    return jsonify(books), 200

@books.route('/books/<book_id>', methods=['PUT'])
@jwt_required()
def modify_book(book_id):
    data = request.get_json()
    book = update_book(book_id, data)
    if book:
        return jsonify({"message": "Book updated", "book": book.title}), 200
    return jsonify({"message": "Book not found"}), 404

@books.route('/books/<book_id>', methods=['DELETE'])
@jwt_required()
def remove_book(book_id):
    if delete_book(book_id):
        return jsonify({"message": "Book deleted"}), 200
    return jsonify({"message": "Book not found"}), 404
