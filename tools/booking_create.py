import requests
from datetime import date, time

API_URL = "http://127.0.0.1:8000/api/v1/bookings/create"

booking_data = {
    "date": date(2025, 1, 22).isoformat(),
    "start_time": time(14, 0).isoformat(),
    "end_time": time(15, 0).isoformat(),
    "room_id": "502",
    "booked_by": "99",
    "participants": ["102", "103"],
    "comment": "Вебинар",
}

try:
    response = requests.post(API_URL, json=booking_data)
    response.raise_for_status()
    print("Успешно создано бронирование!")
    print("Ответ API:", response.json())
except requests.exceptions.HTTPError as e:
    print(f"HTTP ошибка: {e.response.status_code} - {e.response.json().get('detail')}")
except requests.exceptions.RequestException as e:
    print(f"Ошибка подключения: {e}")
