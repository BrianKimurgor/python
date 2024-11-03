from mongoengine import Document, StringField, IntField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField

class Author(EmbeddedDocument):
    name = StringField(required=True)
    birth_date = StringField()  # Keep as String to store date in "YYYY-MM-DD" format

class Publisher(EmbeddedDocument):
    name = StringField(required=True)
    location = StringField()
    website = StringField()

class Rating(EmbeddedDocument):
    user_id = StringField(required=True)
    rating = IntField(min_value=1, max_value=5)
    review = StringField()
    date = StringField()  # Keep as String to store date in "YYYY-MM-DD" format

class Review(EmbeddedDocument):
    user_id = StringField(required=True)
    comment = StringField()
    date = StringField()  # Keep as String to store date in "YYYY-MM-DD" format

class Book(Document):
    title = StringField(required=True)  # Removed unique constraint to allow multiple books with the same title
    author = EmbeddedDocumentField(Author, required=True)
    genre = StringField()
    publication_year = IntField()
    isbn = StringField(required=True, unique=True)  # ISBN should be unique
    price = FloatField()
    stock_quantity = IntField()
    pages = IntField()
    language = StringField()
    publisher = EmbeddedDocumentField(Publisher, required=True)
    description = StringField()
    ratings = ListField(EmbeddedDocumentField(Rating))
    reviews = ListField(EmbeddedDocumentField(Review))
