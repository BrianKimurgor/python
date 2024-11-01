import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.airport_app

def load_data():
    # Load users
    with open("users.json") as f:
        users = json.load(f)["airport_users"]
        for user in users:
            user["password"] = generate_password_hash(user["password"])
        db.users.insert_many(users)
    
    # Load airports
    with open("airport.json") as f:
        airports = json.load(f)["airports"]
        db.airports.insert_many(airports)

if __name__ == "__main__":
    load_data()
    print("Data loaded successfully.")
