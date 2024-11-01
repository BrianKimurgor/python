import json
from bson import ObjectId
from werkzeug.security import generate_password_hash
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.carpark_db

def load_data():
    # Load users
    with open("data/carpark_users.json") as f:
        users = json.load(f)["carpark_users"]
        for user in users:
            # Check if the user already exists
            if db.users.find_one({"username": user["username"]}):
                print(f"User {user['username']} already exists. Skipping.")
                continue
            user["password"] = generate_password_hash(user["password"])
            db.users.insert_one(user)
    
    # Load carpark with ObjectId conversion
    with open("data/carparks.json") as f:
        carparks = json.load(f)["carparks"]
        for carpark in carparks:
            # Check if carpark with the same code already exists
            if db.carparks.find_one({"code": carpark["name"]}):
                print(f"Airport with code {carpark['name']} already exists. Skipping.")
                continue
            carpark["_id"] = ObjectId()  # Generate a new ObjectId for each airport
            carpark.pop("id", None)  # Remove the UUID 'id' field
            db.carparks.insert_one(carpark)

if __name__ == "__main__":
    load_data()
    print("Data loaded successfully.")
