from datetime import date, timedelta, time
import sys
import os

# Исправленный импорт, чтобы работать из директории tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import create_booking, set_data_folder, add_user, save_rooms

# Установим путь для данных
set_data_folder("data")

# Пользователи с nickname и telegram_id
users = [
    {"id": "101", "name": "Петр", "nickname": "Петя", "telegram_id": "@petrov"},
    {"id": "102", "name": "Вася", "nickname": "Васек", "telegram_id": "@vasya"},
    {"id": "103", "name": "Марина Ивановна Вениаминовна", "nickname": "Марина", "telegram_id": "@marina"},
    {"id": "104", "name": "Ольга", "nickname": "Оля", "telegram_id": "@olga"},
]

# Добавляем пользователей в базу
for user in users:
    add_user(user["id"], user["name"], nickname=user["nickname"])

# Комнаты
rooms = [
    {"id": "501", "name": "Переговорная 501", "capacity": 10, "features": ["проектор", "флипчарт"]},
    {"id": "502", "name": "Переговорная 502", "capacity": 6, "features": ["телевизор"]},
]

# Сохраняем комнаты
save_rooms(rooms)

# Даты и временные слоты
dates = [date(2025, 1, 22) + timedelta(days=i) for i in range(5)]  # Следующие 5 дней
time_slots = [
    (time(9, 0), time(10, 0)),
    (time(10, 15), time(11, 15)),
    (time(11, 30), time(12, 30)),
    (time(14, 0), time(15, 0)),
]

# Генерация бронирований
for target_date in dates:
    for room in rooms:
        for slot, user in zip(time_slots, users):
            start_time, end_time = slot
            create_booking({
                "id": f"{room['id']}{target_date.strftime('%Y%m%d')}{start_time.strftime('%H%M')}",
                "room_id": room["id"],
                "date": target_date.strftime("%Y-%m-%d"),
                "start_time": start_time.strftime("%H:%M"),
                "end_time": end_time.strftime("%H:%M"),
                "booked_by": user["id"],
                "participants": [u["id"] for u in users if u["id"] != user["id"]],  # Все, кроме текущего
                "status": "confirmed",
                "comment": f"Бронирование от {user['name']}",
            })

print("Тестовые данные успешно сгенерированы!")
