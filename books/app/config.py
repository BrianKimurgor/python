import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/books_db')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwtsecret')

config = Config()
