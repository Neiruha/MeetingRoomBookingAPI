import requests
from datetime import date, time

# === Настройки запроса ===
API_URL = "http://127.0.0.1:8000/api/v1/plan/"  # Запусти свой FastAPI сервер перед запуском теста


payload = {
    "date": date.today().isoformat(),
    "start_time": time(8, 0).isoformat(),
    "end_time": time(9, 00).isoformat(),
    "min_capacity": 2,
    "needed_interval": 60  # Теперь в JSON, не в params!
}

response = requests.post(API_URL, json=payload)

if response.status_code == 200:
    print("✅ Успех! Ответ сервера:")
    print(response.json())
else:
    print(f"❌ Ошибка {response.status_code}: {response.text}")


# === Обрабатываем ответ ===
if response.status_code == 200:

    print(response.json())

    plan = response.json()
    print("\n=== Свободные переговорки ===")
    for room in plan:
        print(f"\nКомната: {room['room_name']} (ID: {room['room_id']})")
        if "available_slots" in room:
            print("  Доступные слоты:")
            for start, end in room["available_slots"]:
                print(f"    ⏳ {start} - {end}")
        if "alternative_slots" in room:
            print("  🔍 Альтернативные слоты (сдвинули время):")
            for start, end in room["alternative_slots"]:
                print(f"    🕗 {start} - {end}")
else:
    print(f"❌ Ошибка {response.status_code}: {response.text}")
