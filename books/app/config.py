import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/bookstore_db")
    MONGO_DBNAME = os.getenv("MONGO_DBNAME", "bookstore_db")  # Default database name
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
