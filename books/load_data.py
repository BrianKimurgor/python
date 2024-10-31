import json
from mongoengine import connect, disconnect, NotUniqueError
from app.models.book import Book, Author, Publisher, Rating, Review  # Import Book-related models
from app.models.user import User  # Import User model

# Connect to MongoDB
connect("boos_db")  # Replace with your database name

def load_json_data():
    # Load data from JSON files
    with open('data/books_users.json', 'r') as users_file:
        users_data = json.load(users_file)
    
    with open('data/bookstore.json', 'r') as books_file:
        books_data = json.load(books_file)
    
    # Insert users
    for user_data in users_data:
        if not User.objects(username=user_data["username"]).first():  # Check for existing user
            user = User(username=user_data["username"], admin=user_data.get("admin", False))
            user.set_password(user_data["password"])  # Hash the password
            try:
                user.save()
            except NotUniqueError:
                print(f"User '{user.username}' already exists. Skipping...")
        else:
            print(f"User '{user_data['username']}' already exists. Skipping...")

    # Insert books
    for book_data in books_data.get("books", []):
        # Create Author, Publisher, Ratings, and Reviews objects
        author_data = book_data.get("author")
        publisher_data = book_data.get("publisher")
        ratings_data = book_data.get("ratings", [])
        reviews_data = book_data.get("reviews", [])
        
        # Create embedded document instances
        author = Author(**author_data) if author_data else None
        publisher = Publisher(**publisher_data) if publisher_data else None
        ratings = [Rating(**rating) for rating in ratings_data]
        reviews = [Review(**review) for review in reviews_data]

        # Check if the book already exists
        if not Book.objects(title=book_data["title"]).first():
            # Create and save the Book instance
            book = Book(
                title=book_data["title"],
                author=author,
                genre=book_data.get("genre"),
                publication_year=book_data.get("publication_year"),
                isbn=book_data.get("isbn"),
                price=book_data.get("price"),
                stock_quantity=book_data.get("stock_quantity"),
                pages=book_data.get("pages"),
                language=book_data.get("language"),
                publisher=publisher,
                description=book_data.get("description"),
                ratings=ratings,
                reviews=reviews
            )
            try:
                book.save()
            except NotUniqueError:
                print(f"Book with title '{book.title}' already exists. Skipping...")
        else:
            print(f"Book with title '{book_data['title']}' already exists. Skipping...")

    print("Data loaded successfully.")

if __name__ == "__main__":
    load_json_data()
    disconnect()
