from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from app.models.book import Book

book_bp = Blueprint('bookstore_db', __name__)

# Helper function to serialize embedded documents
def serialize_book(book):
    return {
        'id': str(book.id),
        'title': book.title,
        'author': book.author.to_mongo() if book.author else None,  # Convert embedded document to dict
        'genre': book.genre,
        'publication_year': book.publication_year,
        'isbn': book.isbn,
        'price': book.price,
        'stock_quantity': book.stock_quantity,
        'pages': book.pages,
        'language': book.language,
        'publisher': book.publisher.to_mongo() if book.publisher else None,  # Convert embedded document to dict
        'description': book.description,
        'ratings': [rating.to_mongo() for rating in book.ratings],  # Convert list of embedded documents
        'reviews': [review.to_mongo() for review in book.reviews]  # Convert list of embedded documents
    }

# Add a new book (admin only)
@book_bp.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    """
    Adds a new book to the database.
    
    Requires admin access. Retrieves book data from the request and creates
    a Book instance with it, then saves it to the database.
    """

    data = request.get_json()
    try:
        # Create the Book instance with embedded documents
        book = Book(
            title=data['title'],
            author={
                "name": data['author']['name'],
                "birth_date": data['author'].get('birth_date')
            },
            genre=data['genre'],
            publication_year=data['publication_year'],
            isbn=data['isbn'],
            price=data['price'],
            stock_quantity=data['stock_quantity'],
            pages=data['pages'],
            language=data['language'],
            publisher={
                "name": data['publisher']['name'],
                "location": data['publisher'].get('location'),
                "website": data['publisher'].get('website')
            },
            description=data['description'],
            ratings=[],  # Start with an empty list of ratings
            reviews=[]   # Start with an empty list of reviews
        )
        book.save()
        return jsonify({"message": "Book added successfully", "book_id": str(book.id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Retrieve all books
@book_bp.route('/books', methods=['GET'])
def get_books():
    """
    Retrieve a list of books with their details.
    """
    try:
        books = Book.objects()
        return jsonify([serialize_book(book) for book in books]), 200
    except Exception as e:
        print("Error occurred:", str(e))  # Debug line
        return jsonify({"error": str(e)}), 500

# Update a book by ID (admin only)
@book_bp.route('/books/<id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    """
    Updates a book's details by ID, requiring admin access.
    """

    data = request.get_json()
    try:
        book = Book.objects(id=id).first()
        if not book:
            return jsonify({"error": "Book not found"}), 404
        
        # Update the book fields
        book.update(
            title=data.get('title', book.title),
            author=data.get('author', book.author),  # You might want to handle author updates more specifically
            genre=data.get('genre', book.genre),
            publication_year=data.get('publication_year', book.publication_year),
            isbn=data.get('isbn', book.isbn),
            price=data.get('price', book.price),
            stock_quantity=data.get('stock_quantity', book.stock_quantity),
            pages=data.get('pages', book.pages),
            language=data.get('language', book.language),
            publisher=data.get('publisher', book.publisher),  # Similar handling for publisher
            description=data.get('description', book.description)
        )
        return jsonify({"message": "Book updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a book by ID (admin only)
@book_bp.route('/books/<id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    """
    Deletes a book by ID, requiring admin access.
    """
    claims = get_jwt()

    try:
        book = Book.objects(id=id).first()
        if not book:
            return jsonify({"error": "Book not found"}), 404
        
        book.delete()
        return jsonify({"message": "Book deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Search for books by title, genre, or author
@book_bp.route('/books/search', methods=['GET'])
def search_books():
    """
    Searches for books by title, genre, or author.
    """
    title = request.args.get('title')
    genre = request.args.get('genre')
    author = request.args.get('author')
    query = {}

    if title:
        query['title__icontains'] = title
    if genre:
        query['genre__icontains'] = genre
    if author:
        query['author__name__icontains'] = author

    try:
        books = Book.objects(**query)
        return jsonify([serialize_book(book) for book in books]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
