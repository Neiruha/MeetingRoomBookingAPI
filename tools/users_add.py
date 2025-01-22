import requests

API_URL = "http://127.0.0.1:8000/api/v1/users/add"

users = [
    {"id": "205", "name": "Анна", "nickname": "Аня"},
    {"id": "206", "name": "Игорь", "nickname": "Игоша"},
]

for user_data in users:
    try:
        response = requests.post(API_URL, json=user_data)
        response.raise_for_status()
        print(f"Успешно добавлен пользователь {user_data['name']}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка: {e.response.status_code} - {e.response.json().get('detail')}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения: {e}")
