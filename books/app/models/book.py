from mongoengine import Document, StringField, IntField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField

class Author(EmbeddedDocument):
    name = StringField(required=True)
    birth_date = StringField()

class Publisher(EmbeddedDocument):
    name = StringField(required=True)
    location = StringField()
    website = StringField()

class Rating(EmbeddedDocument):
    user_id = StringField(required=True)
    rating = IntField(min_value=1, max_value=5)
    review = StringField()
    date = StringField()

class Review(EmbeddedDocument):
    user_id = StringField(required=True)
    comment = StringField()
    date = StringField()

class Book(Document):
    title = StringField(required=True, unique=True)
    author = EmbeddedDocumentField(Author)
    genre = StringField()
    publication_year = IntField()
    isbn = StringField(unique=True)
    price = FloatField()
    stock_quantity = IntField()
    pages = IntField()
    language = StringField()
    publisher = EmbeddedDocumentField(Publisher)
    description = StringField()
    ratings = ListField(EmbeddedDocumentField(Rating))
    reviews = ListField(EmbeddedDocumentField(Review))
