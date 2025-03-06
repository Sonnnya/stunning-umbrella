import os
import requests


def main():
    server_url = "http://server:5000"
    # Вместо ввода из консоли используем имя из переменной окружения или значение по умолчанию
    name = os.environ.get("USER_NAME", "TestUser")

    print(f"Отправка запроса на добавление пользователя с именем: {name}")
    try:
        # Отправляем POST-запрос, как если бы заполнили форму index.html
        post_response = requests.post(f"{server_url}/add", data={"name": name})
        if post_response.status_code in (200, 302):
            print("Пользователь успешно добавлен!")
        else:
            print("Ошибка при добавлении пользователя, статус:",
                  post_response.status_code)
    except Exception as e:
        print("Ошибка подключения к серверу при отправке POST-запроса:", e)
        return

    try:
        # Получаем страницу index.html, чтобы увидеть обновленный список пользователей
        get_response = requests.get(f"{server_url}/")
        if get_response.ok:
            print("Получена страница index.html:")
            print(get_response.text)
        else:
            print("Ошибка при получении страницы, статус:",
                  get_response.status_code)
    except Exception as e:
        print("Ошибка подключения к серверу при получении страницы:", e)


if __name__ == "__main__":
    main()
