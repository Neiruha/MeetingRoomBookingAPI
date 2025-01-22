import requests

API_URL = "http://127.0.0.1:8000/api/v1/rooms/add"

rooms = [
    {"id": "503", "name": "Переговорная 503", "capacity": 8, "features": ["флипчарт"]},
    {"id": "504", "name": "Переговорная 504", "capacity": 12, "features": ["проектор", "телевизор"]},
]

for room_data in rooms:
    try:
        response = requests.post(API_URL, json=room_data)
        response.raise_for_status()
        print(f"Успешно добавлена комната {room_data['name']}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка: {e.response.status_code} - {e.response.json().get('detail')}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения: {e}")
