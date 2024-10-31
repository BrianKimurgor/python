from models.book import Book, Author, Publisher
from bson import ObjectId

def create_book(data):
    author = Author(**data['author'])
    publisher = Publisher(**data['publisher'])
    book = Book(
        title=data['title'],
        author=author,
        genre=data['genre'],
        publication_year=data['publication_year'],
        isbn=data['isbn'],
        price=data['price'],
        stock_quantity=data['stock_quantity'],
        pages=data['pages'],
        language=data['language'],
        publisher=publisher,
        description=data['description']
    )
    book.save()
    return book

def get_books():
    books = Book.objects()
    books_list = []
    for boo in books:
        # Convert the ObjectId to a string
        book_dict = boo.to_mongo().to_dict()
        book_dict['_id'] = str(book_dict['_id'])  # Ensure _id is a string
        books_list.append(book_dict)
    return books_list

def update_book(book_id, data):
    book = Book.objects(id=book_id).first()
    if book:
        book.update(**data)
        book.reload()
        return book
    return None

def delete_book(book_id):
    book = Book.objects(id=book_id).first()
    if book:
        book.delete()
        return True
    return False
