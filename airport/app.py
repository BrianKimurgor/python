from flask import Flask
from flask_jwt_extended import JWTManager
from mongoengine import connect
from app.config import Config
from app.routes.user_route import user_bp
from app.routes.airport_route import airport_bp

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

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(airport_bp, url_prefix='/api')

# Home route
@app.route("/")
def home():
    return {"message": "Welcome to the Airport API"}, 200

# Run the application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
