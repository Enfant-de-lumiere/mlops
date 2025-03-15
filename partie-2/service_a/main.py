from flask import Flask, render_template, request, redirect, jsonify
import requests

SERVICE_B_URL = "http://service_b"

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/authenticate", methods=["POST"])
def authenticate():
    data = request.json
    response = requests.post(f"{SERVICE_B_URL}/authenticate", json=data)
    return response.json()

@app.route("/data", methods=["GET"])
def get_data():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token manquant"}), 401

    response = requests.get(f"{SERVICE_B_URL}/data", headers={"Authorization": token})
    return response.json()
