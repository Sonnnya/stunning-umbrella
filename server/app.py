from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import create_engine, text
import os

app = Flask(__name__)

# Получаем URL для подключения к БД из переменных окружения
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///:memory:")
engine = create_engine(DATABASE_URL)


@app.route("/", methods=["GET"])
def index():
    # Получаем список пользователей для отображения на странице
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, name FROM users"))
        users = [{"id": row[0], "name": row[1]} for row in result.fetchall()]
    return render_template("index.html", users=users)


@app.route("/add", methods=["POST"])
def add_user():
    # Извлекаем имя из данных формы
    name = request.form.get("name")
    if name:
        # Используем транзакцию для вставки данных в базу
        with engine.begin() as connection:
            connection.execute(
                text("INSERT INTO users (name) VALUES (:name)"),
                {"name": name}
            )
        # После добавления возвращаемся на главную страницу
        return redirect(url_for("index"))
    else:
        return "Имя обязательно для заполнения", 400


if __name__ == "__main__":
    # Запуск сервера на 0.0.0.0 для доступности из контейнера
    app.run(host="0.0.0.0", port=5000)
