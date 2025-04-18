import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/user/<name>')
def get_user(name):
    res = requests.get(f'http://localhost:3500/v1.0/invoke/user-service/method/get/{name}')
    return jsonify(res.json())

app.run(port=5000)
