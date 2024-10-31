from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient

# Initialize Flask and other components
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"  # Change this!
jwt = JWTManager(app)

# MongoDB client
client = MongoClient("mongodb://localhost:27017")
db = client["your_database_name"]

# Import routes
from app.routes.books import books

# Register blueprints
app.register_blueprint(books, url_prefix="/api/books")

# app.register_blueprint(carparks.bp, url_prefix="/api/carparks")
# app.register_blueprint(airports.bp, url_prefix="/api/airports")
