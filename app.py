from flask import Flask, jsonify, request
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


@app.route("/api/applications", methods=["POST"])
def add_application():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"message": "Request must contain JSON object!"}), 400
    if not data.get("company") or not data.get("role"):
        return jsonify({"message": "Invalid entry!"}), 400
    conn = get_connection()
    conn.execute("INSERT INTO applications (company, role) VALUES (?, ?)", (data["company"], data["role"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Application added!"}), 201


@app.route("/api/applications/<int:id>")
def get_application(id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM applications WHERE id = ?", (id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({"message": "Application does not exist!"}), 404
    else:
        conn.close()
        return jsonify(dict(row))


@app.route("/api/applications/<int:id>", methods=["DELETE"])
def delete_application(id):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM applications WHERE id = ?", (id,))
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"message": "Cannot delete because application does not exist!"}), 404
    else:
        conn.commit()
        conn.close()
        return jsonify({"message": "Successfully deleted!"}), 200


@app.route("/api/applications/<int:id>", methods=["PUT"])
def update_application(id):
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"message": "Request must contain JSON object!"}), 400
    if not data.get("company") or not data.get("role"):
        return jsonify({"message": "Company or Role are invalid!"}), 400
    else:
        conn = get_connection()
        cursor = conn.execute("UPDATE applications SET company = ?, role = ? WHERE id = ?", (data["company"], data["role"], id))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"message": "Cannot edit because application does not exist!"}), 404
        else:
            conn.close()
            return jsonify({"message": "Successfully edited!"}), 200

