import json
from bson import ObjectId
from werkzeug.security import generate_password_hash
from pymongo import MongoClient
import os

client = MongoClient("mongodb://localhost:27017/")
db = client.carpark_db

def load_data():
    """
    Load user and carpark data from JSON files into the database.

    This function performs the following operations:
    - Loads user data from 'data/carpark_users.json' and inserts it into the 'users' collection
        in the database. If a user with the same username already exists, it skips that user.
    - Loads carpark data from 'data/carparks.json' and inserts it into the 'carparks' collection
        in the database. If a carpark with the same code already exists, it skips that carpark.
        Each carpark is assigned a new ObjectId, and the original UUID 'id' field is removed.
    """
    file_path = os.path.join(os.path.dirname(__file__), "data/carpark_users.json")
    with open(file_path) as f:
        users = json.load(f)["carpark_users"]
        for user in users:
            # Check if the user already exists
            if db.users.find_one({"username": user["username"]}):
                print(f"User {user['username']} already exists. Skipping.")
                continue
            user["password"] = generate_password_hash(user["password"])
            db.users.insert_one(user)
    
    # Load carpark with ObjectId conversion
    file_path = os.path.join(os.path.dirname(__file__), "data/carparks.json")
    with open(file_path) as f:
        carparks = json.load(f)["carparks"]
        for carpark in carparks:
            # Check if carpark with the same code already exists
            if db.carparks.find_one({"code": carpark["name"]}):
                print(f"Airport with code {carpark['name']} already exists. Skipping.")
                continue
            carpark["_id"] = ObjectId()  # Generate a new ObjectId for each carpark
            carpark.pop("id", None)  # Remove the UUID 'id' field
            db.carparks.insert_one(carpark)

if __name__ == "__main__":
    load_data()
    print("Data loaded successfully.")
