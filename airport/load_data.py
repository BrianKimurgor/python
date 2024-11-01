import json
from bson import ObjectId
from werkzeug.security import generate_password_hash
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.airport_app

def load_data():
    # Load users
    with open("data/airport_users.json") as f:
        users = json.load(f)["airport_users"]
        for user in users:
            # Check if the user already exists
            if db.users.find_one({"username": user["username"]}):
                print(f"User {user['username']} already exists. Skipping.")
                continue
            user["password"] = generate_password_hash(user["password"])
            db.users.insert_one(user)
    
    # Load airports with ObjectId conversion
    with open("data/airports.json") as f:
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
