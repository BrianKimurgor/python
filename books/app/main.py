from flask import Flask
from mongoengine import connect
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp
from routes.books import books_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

connect('bookstore_db', host='localhost', port=27017)

jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(books_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
