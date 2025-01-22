import requests
from datetime import datetime, time

# Настройки
API_URL = "http://127.0.0.1:8000/api/v1"
CHECK_DATE = datetime(2025, 1, 22).date()
START_TIME = time(14, 0)
END_TIME = time(15, 0)
MIN_CAPACITY = None  # Минимальная вместимость (None, если фильтрация не нужна)

def format_booking(booking):
    """Форматировать бронирование для вывода."""
    participants = ", ".join([p["name"] for p in booking.get("participants", [])])
    guests = ", ".join(booking.get("guests", []))
    booked_by = booking["booked_by"]["name"]

    return (f"- Комната {booking['room_id']} занята с {booking['start_time']} до {booking['end_time']} "
            f"({booking['comment']}).\n"
            f"  Забронировал: {booked_by}\n"
            f"  Участники: {participants or 'нет'}\n"
            f"  Гости: {guests or 'нет'}")

def check_availability():
    """Проверка доступности переговорок."""
    print(f"Проверяем доступность комнат на {CHECK_DATE} с {START_TIME} до {END_TIME}...\n")
    
    try:
        # Запрос на проверку доступности
        response = requests.post(
            f"{API_URL}/availability/",
            json={
                "date": str(CHECK_DATE),
                "start_time": START_TIME.strftime("%H:%M"),
                "end_time": END_TIME.strftime("%H:%M"),
                "min_capacity": MIN_CAPACITY,
            },
        )
        response.raise_for_status()

        available_rooms = response.json()
        if available_rooms:
            print("Доступные комнаты:")
            for room in available_rooms:
                print(f"- {room['name']} (вместимость: {room['capacity']}, особенности: {', '.join(room['features'])})")
        else:
            print("Нет доступных комнат на указанное время.")

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:  # Если комнаты заняты
            print("Все комнаты заняты. Смотрим текущее расписание...\n")

            # Запрос на бронирования
            response = requests.get(f"{API_URL}/bookings/all")
            response.raise_for_status()
            bookings = response.json()

            # Фильтруем бронирования на указанное время
            overlapping_bookings = [
                b for b in bookings
                if b["date"] == str(CHECK_DATE) and
                   b["start_time"] < END_TIME.strftime("%H:%M") and
                   b["end_time"] > START_TIME.strftime("%H:%M")
            ]

            for booking in overlapping_bookings:
                print(format_booking(booking))
        else:
            print(f"Ошибка HTTP: {e.response.status_code} - {e.response.json().get('detail')}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения с API: {e}")

if __name__ == "__main__":
    check_availability()
