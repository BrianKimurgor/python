import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/airport_app")
    MONGO_DBNAME = os.getenv("MONGO_DBNAME", "airport_app")  # Default database name
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
