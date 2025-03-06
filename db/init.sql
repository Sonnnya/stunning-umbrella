-- Создание таблицы users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Вставка примера пользователя
INSERT INTO users (name) VALUES ('Alice');
