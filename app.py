from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, internship tracker!"


@app.route("/api/applications")
def applications():
    return jsonify([])