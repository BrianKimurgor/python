# app.py
from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from app.config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB client
mongo_client = MongoClient(app.config["MONGO_URI"])
db = mongo_client.get_database()  # Get the default database from the URI

# Initialize JWT manager
jwt = JWTManager(app)


# Home route
@app.route("/")
def home():
    return {"message": "Welcome to the Airport API"}, 200

# Run the application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
