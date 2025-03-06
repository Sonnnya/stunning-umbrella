from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2
import logging
import os

app = Flask(__name__)
CORS(app)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Подключение к базе данных
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://myuser:mypassword@db:5432/mydb")


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    conn.commit()
    cur.close()
    conn.close()

    logging.info(f"User added: {name}")
    return jsonify({"message": "User added successfully"})


@app.route("/get_users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users")
    users = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()

    logging.info(f"Users retrieved: {users}")
    return jsonify(users)


@app.route("/delete_user", methods=["POST"])
def delete_user():
    data = request.json
    user_id = data.get("id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

    logging.info(f"User deleted: {user_id}")
    return jsonify({"message": "User deleted successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
