from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["users_db"]
users = db["users"]

@app.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()
    users.insert_one(data)
    return jsonify({"message": "User added!"})

@app.route('/get/<name>', methods=['GET'])
def get_user(name):
    user = users.find_one({"name": name}, {"_id": 0})
    return jsonify(user or {"error": "User not found"})

app.run(port=5001)
