from flask import Flask, render_template

SERVICE_B_URL = "http://service_b"

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

