import requests
from datetime import date, time

API_URL = "http://127.0.0.1:8000/api/v1/bookings/create"

booking_data = {
    "date": date(2025, 2, 5).isoformat(),
    "start_time": time(16, 0).isoformat(),
    "end_time": time(17, 0).isoformat(),
    "room_id": "501",
    "booked_by": "103",
    "participants": ["102"],
    "comment": "Вебинар",
}

booking_data = {
  "date": "2025-02-05",
  "start_time": "16:30",
  "end_time": "17:30",
  "room_id": "502",
  "booked_by": "104",
  "participants": ["103"],  
  "comment": "Тайная встреча Снегурочки и Деда Мороза"
}

try:
    response = requests.post(API_URL, json=booking_data)

    print(response.json())

    response.raise_for_status()
    print("Успешно создано бронирование!")
    print("Ответ API:", response.json())
except requests.exceptions.HTTPError as e:
    print(f"HTTP ошибка: {e.response.status_code} - {e.response.json().get('detail')}")
except requests.exceptions.RequestException as e:
    print(f"Ошибка подключения: {e}")
