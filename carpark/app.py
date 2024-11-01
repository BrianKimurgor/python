from flask import Flask
from flask_jwt_extended import JWTManager
from mongoengine import connect
from app.config import Config


# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoEngine connection
connect(
    db=app.config["MONGO_DBNAME"],   # Database name
    host=app.config["MONGO_URI"]     # MongoDB URI
)

# Initialize JWT manager
jwt = JWTManager(app)


# Home route
@app.route("/")
def home():
    return {"message": "Welcome to the Carpark API"}, 200

# Run the application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
