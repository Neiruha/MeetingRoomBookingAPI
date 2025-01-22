from datetime import date, timedelta, time
from app.database import create_booking, set_data_folder, add_user, save_rooms

# Установим путь для данных
set_data_folder("./data")

# Определяем комнаты
rooms = [
    {
        "id": "501",
        "name": "Переговорная 501",
        "capacity": 10,
        "features": ["проектор", "флипчарт"],
    },
    {
        "id": "502",
        "name": "Переговорная 502",
        "capacity": 6,
        "features": ["телевизор"],
    },
]

# Сохраняем комнаты
save_rooms(rooms)
print("Комнаты успешно созданы!")

# Пользователи
users = {
    101: "Петр",
    102: "Вася",
    103: "Марина Ивановна Вениаминовна",
    104: "Ольга",
}

# Добавляем пользователей в базу
for user_id, name in users.items():
    add_user(user_id, name)
    print(f"Добавлен пользователь: {name} (ID: {user_id})")

# Даты бронирований
dates = [date(2025, 1, 18) + timedelta(days=i) for i in range(7)]  # 18–24 января

# Временные слоты
time_slots = [
    (time(9, 0), time(10, 0)),
    (time(10, 15), time(11, 15)),
    (time(11, 30), time(12, 30)),
    (time(14, 0), time(15, 0)),
    (time(15, 30), time(16, 30)),
]

# Примерное расписание участников
schedule = [
    (101, [103]),  # Петр с Мариной
    (102, [101]),  # Вася с Петром
    (103, [104]),  # Марина с Ольгой
    (104, [102]),  # Ольга с Васей
    (101, [101]),  # Петр сам с собой (фиктивный участник)
]

# Генерация бронирований
for target_date in dates:
    for room in rooms:
        for slot, (booked_by, participants) in zip(time_slots, schedule):
            # Если список участников пуст, добавляем "фиктивного гостя"
            if not participants:
                participants = [101]  # Добавляем Петра как фиктивного участника
                print(f"У бронирования не было участников, добавлен Петр (ID: 101)")

            booking_data = {
                "id": f"{room['id']}{target_date.strftime('%Y%m%d')}{slot[0].strftime('%H%M')}",
                "room_id": room["id"],
                "date": target_date.strftime("%Y-%m-%d"),
                "start_time": slot[0].strftime("%H:%M"),
                "end_time": slot[1].strftime("%H:%M"),
                "booked_by": booked_by,
                "participants": participants,
                "status": "confirmed",
                "comment": "Тестовое бронирование",
            }
            try:
                create_booking(booking_data)
                print(
                    f"Создано бронирование: ID {booking_data['id']} для комнаты {room['id']} на дату {target_date}"
                )
            except ValueError as e:
                print(f"Ошибка при создании бронирования: {e}")

print("Тестовые данные успешно созданы!")
