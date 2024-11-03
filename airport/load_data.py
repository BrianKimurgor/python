import json
from bson import ObjectId
from werkzeug.security import generate_password_hash
from pymongo import MongoClient
import os

client = MongoClient("mongodb://localhost:27017/")
db = client.airport_app

def load_data():
    """
    Load user and airport data from JSON files into the database.

    This function performs the following operations:
    - Loads user data from 'airport_users.json' and inserts each user into the 'users' collection
        in the database. If a user with the same username already exists, that user is skipped.
        Passwords are hashed before insertion.
    - Loads airport data from 'airports.json' and inserts each airport into the 'airports' collection
        in the database. If an airport with the same code already exists, that airport is skipped.
        Each airport is assigned a new [ObjectId](https://www.mongodb.com/docs/manual/reference/object-id/), and any existing 'id' field is removed.

    Note:
    - The JSON files are expected to be located in a 'data' directory relative to the script's location.
    - The database operations assume the existence of 'users' and 'airports' collections.
    - The function uses 'generate_password_hash' for password hashing and 'ObjectId' for generating
        unique identifiers for airports.
    """
    file_path = os.path.join(os.path.dirname(__file__), "data/airport_users.json")
    with open(file_path) as f:
        users = json.load(f)["airport_users"]
        for user in users:
            # Check if the user already exists
            if db.users.find_one({"username": user["username"]}):
                print(f"User {user['username']} already exists. Skipping.")
                continue
            user["password"] = generate_password_hash(user["password"])
            db.users.insert_one(user)
    
    # Load airports with ObjectId conversion
    file_path = os.path.join(os.path.dirname(__file__), "data/airports.json")
    with open(file_path) as f:
        airports = json.load(f)["airports"]
        for airport in airports:
            # Check if an airport with the same code already exists
            if db.airports.find_one({"code": airport["code"]}):
                print(f"Airport with code {airport['code']} already exists. Skipping.")
                continue
            airport["_id"] = ObjectId()  # Generate a new ObjectId for each airport
            airport.pop("id", None)  # Remove the UUID 'id' field
            db.airports.insert_one(airport)

if __name__ == "__main__":
    load_data()
    print("Data loaded successfully.")
