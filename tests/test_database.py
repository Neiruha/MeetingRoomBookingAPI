import os
import pytest
from datetime import date, time
from app.database import (
    create_booking,
    get_booking,
    delete_booking,
    check_room_availability,
    get_user_bookings,
    get_bookings_in_range,
    write_bookings,
    read_bookings,
    set_data_folder,
    add_user,
    process_participants,
    load_users
)

# Преобразование TEST_DATA_FOLDER в абсолютный путь
TEST_DATA_FOLDER = os.path.abspath("./test_data")

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """Настройка тестовой среды: создание и удаление тестовой папки."""
    set_data_folder(TEST_DATA_FOLDER)  # Используем тестовую папку
    os.makedirs(TEST_DATA_FOLDER, exist_ok=True)
    yield
    for file in os.listdir(TEST_DATA_FOLDER):
        os.remove(os.path.join(TEST_DATA_FOLDER, file))
    os.rmdir(TEST_DATA_FOLDER)

def test_create_booking():
    # Добавляем пользователя в базу
    add_user(123, "Test User")

    booking = {
        "id": "501202501170900",
        "room_id": "501",
        "date": "2025-01-17",
        "start_time": "09:00",
        "end_time": "10:00",
        "booked_by": "123",  # ID добавленного пользователя
        "participants": ["Alice", "Bob"],
        "status": "confirmed",
        "comment": "Important meeting",
    }
    
    # Создаём бронирование
    result = create_booking(booking)
    
    # Проверяем, что бронирование создано корректно
    assert result["id"] == "501202501170900"

    # Проверяем, что данные сохранились в файле
    bookings = read_bookings(date(2025, 1, 17))
    assert len(bookings) == 1
    assert bookings[0]["id"] == "501202501170900"

    # Попытка создать дубликат должна завершиться ошибкой
    with pytest.raises(ValueError):
        create_booking(booking)

def test_get_booking():
    booking = {
        "id": "501202501170900",
        "room_id": "501",
        "date": "2025-01-17",
        "start_time": "09:00",
        "end_time": "10:00",
        "booked_by": "user_123",
        "participants": ["Alice", "Bob"],
        "status": "confirmed",
        "comment": "Important meeting",
    }
    write_bookings(date(2025, 1, 17), [booking])
    result = get_booking(date(2025, 1, 17), "501202501170900")
    assert result == booking

def test_delete_booking():
    booking = {
        "id": "501202501170900",
        "room_id": "501",
        "date": "2025-01-17",
        "start_time": "09:00",
        "end_time": "10:00",
        "booked_by": "user_123",
        "participants": ["Alice", "Bob"],
        "status": "confirmed",
        "comment": "Important meeting",
    }
    write_bookings(date(2025, 1, 17), [booking])
    deleted = delete_booking(date(2025, 1, 17), "501202501170900")
    assert deleted is True
    remaining = read_bookings(date(2025, 1, 17))
    assert len(remaining) == 0

def test_check_room_availability():
    booking = {
        "id": "501202501170900",
        "room_id": "501",
        "date": "2025-01-17",
        "start_time": "09:00",
        "end_time": "10:00",
        "booked_by": "user_123",
        "participants": ["Alice", "Bob"],
        "status": "confirmed",
        "comment": "Important meeting",
    }
    write_bookings(date(2025, 1, 17), [booking])

    # Проверка на пересечение времени
    available = check_room_availability(
        date(2025, 1, 17), "501", time(10, 0), time(11, 0)
    )
    assert available is True

    not_available = check_room_availability(
        date(2025, 1, 17), "501", time(9, 30), time(10, 0)
    )
    assert not_available is False

def test_get_user_bookings():
    bookings = [
        {
            "id": "501202501170900",
            "room_id": "501",
            "date": "2025-01-17",
            "start_time": "09:00",
            "end_time": "10:00",
            "booked_by": "user_123",
            "participants": ["Alice", "Bob"],
            "status": "confirmed",
            "comment": "Meeting A",
        },
        {
            "id": "502202501171000",
            "room_id": "502",
            "date": "2025-01-17",
            "start_time": "10:00",
            "end_time": "11:00",
            "booked_by": "user_456",
            "participants": ["Charlie", "Dave"],
            "status": "confirmed",
            "comment": "Meeting B",
        },
    ]
    write_bookings(date(2025, 1, 17), bookings)

    user_bookings = get_user_bookings("user_123", date(2025, 1, 16), date(2025, 1, 17))
    assert len(user_bookings) == 1
    assert user_bookings[0]["id"] == "501202501170900"

def test_get_bookings_in_range():
    bookings_day1 = [
        {
            "id": "501202501160900",
            "room_id": "501",
            "date": "2025-01-16",
            "start_time": "09:00",
            "end_time": "10:00",
            "booked_by": "user_123",
            "participants": ["Alice", "Bob"],
            "status": "confirmed",
            "comment": "Meeting A",
        }
    ]
    bookings_day2 = [
        {
            "id": "502202501171000",
            "room_id": "502",
            "date": "2025-01-17",
            "start_time": "10:00",
            "end_time": "11:00",
            "booked_by": "user_456",
            "participants": ["Charlie", "Dave"],
            "status": "confirmed",
            "comment": "Meeting B",
        }
    ]
    write_bookings(date(2025, 1, 16), bookings_day1)
    write_bookings(date(2025, 1, 17), bookings_day2)

    all_bookings = get_bookings_in_range(date(2025, 1, 16), date(2025, 1, 17))
    assert len(all_bookings) == 2
    assert all_bookings[0]["id"] == "501202501160900"
    assert all_bookings[1]["id"] == "502202501171000"

def test_process_participants():
    add_user(123, "Alice")
    add_user(456, "Bob")

    users = load_users()
    print(f"Users loaded: {users}")
    assert "123" in users, "User 123 not found in users.json"
    assert "456" in users, "User 456 not found in users.json"

    participants = [123, 456, 789, "Charlie"]  # Добавим явный 456
    print(f"Participants: {participants}, types: {[type(p) for p in participants]}")

    known, guests = process_participants(participants, users)
    print(f"Known participants: {known}")
    print(f"Guest participants: {guests}")

    assert len(known) == 2, f"Expected 2 known participants, got {len(known)}"
    assert known[0]["id"] == 123
    assert known[1]["id"] == 456
    assert len(guests) == 2
    assert guests[0] == "Unknown ID: 789"
    assert guests[1] == "Charlie"


def test_add_user():
    # Добавляем первого пользователя
    add_user(123, "Alice")
    users = load_users()
    assert "123" in users, f"User 123 not found, users: {users}"
    assert users["123"]["name"] == "Alice"

    # Добавляем второго пользователя
    add_user(456, "Bob")
    users = load_users()
    assert "456" in users, f"User 456 not found, users: {users}"
    assert users["456"]["name"] == "Bob"
