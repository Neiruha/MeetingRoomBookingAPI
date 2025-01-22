import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_availability():
    """
    Тест доступности переговорок на заданное время.
    """
    url = f"{BASE_URL}/availability/"
    payload = {
        "date": "2025-01-19",
        "start_time": "10:00:00",
        "end_time": "11:00:00",
        "min_capacity": 8
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:", response.json())

def test_urgent_rooms():
    """
    Тест получения списка срочных переговорок.
    """
    url = f"{BASE_URL}/rooms/urgent/"
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:", response.json())

def test_create_booking():
    """
    Тест создания нового бронирования.
    """
    url = f"{BASE_URL}/bookings/"
    payload = {
        "date": "2025-01-19",
        "start_time": "09:00:00",  # Изменяем время, чтобы избежать пересечений
        "end_time": "10:00:00",
        "room_id": "501",
        "participants": ["102", "103"],  # Приводи участников к строкам
        "comment": "Тестовое бронирование"
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:", response.json())

def test_user_bookings(user_id, start_date, end_date):
    """
    Тест получения бронирований для конкретного пользователя за период.
    """
    url = f"{BASE_URL}/bookings/user/"
    payload = {
        "user_id": user_id,
        "start_date": start_date,
        "end_date": end_date
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:", response.json())

def test_error_handling():
    """
    Тест обработки ошибок, например, неверный ID комнаты.
    """
    url = f"{BASE_URL}/bookings/"
    payload = {
        "date": "2025-01-19",
        "start_time": "09:00:00",
        "end_time": "10:00:00",
        "room_id": "999",  # Несуществующая комната
        "participants": ["102", "103"],
        "comment": "Тест с ошибкой"
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:", response.json())

if __name__ == "__main__":
    print("=== Тест доступности переговорок ===")
    test_availability()
    
    print("\n=== Тест срочных переговорок ===")
    test_urgent_rooms()
    
    print("\n=== Тест создания бронирования ===")
    test_create_booking()
    
    print("\n=== Тест бронирований для пользователя ===")
    test_user_bookings("102", "2025-01-17", "2025-01-20")
    
    print("\n=== Тест обработки ошибок ===")
    test_error_handling()
