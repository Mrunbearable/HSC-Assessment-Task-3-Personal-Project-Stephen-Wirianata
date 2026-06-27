#Imports json and os files for reliable data management
import json
import os

#Creates a user file to store data for all users
USER_FILE = "users.json"

#Loads the user from json file if the user file exist, otherwise creates a new json file, adding the new user
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

#Saves the new user for once user has passed authentication system
def save_users(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=4)