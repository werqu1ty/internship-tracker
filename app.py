from flask import Flask, jsonify
from db import get_connection
import sqlite3

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, internship tracker!"


@app.route("/api/applications")
def applications():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM applications").fetchall()
    data = []
    for row in rows:
        data.append(dict(row))
    conn.close()
    return jsonify(data)