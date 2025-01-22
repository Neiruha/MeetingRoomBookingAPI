from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, time, timedelta, date  # Добавили date
from app.schemas import AvailabilityCheck
from app.models import Room, Booking
from app.database import check_room_availability, load_rooms, get_user_bookings


router = APIRouter()

@router.post("/availability/", response_model=List[Room])
async def check_availability_endpoint(check: AvailabilityCheck):
    """
    Проверка доступных переговорок на указанное время.
    """
    # Используем дату из `check.date` напрямую
    target_date = check.date
    start_time = check.start_time
    end_time = check.end_time

    # Загружаем комнаты из JSON
    all_rooms = [Room(**room) for room in load_rooms()]

    # Проверяем доступность каждой комнаты
    available_rooms = [
        room for room in all_rooms
        if check_room_availability(target_date, room.id, start_time, end_time)
    ]

    # Фильтруем по минимальной вместимости
    if check.min_capacity:
        available_rooms = [room for room in available_rooms if room.capacity >= check.min_capacity]

    if not available_rooms:
        raise HTTPException(status_code=404, detail="No available rooms for the given time and capacity")

    return available_rooms


@router.get("/rooms/urgent/", response_model=List[Room])
async def get_urgent_rooms_endpoint():
    """
    Получение списка доступных переговорок в ближайшие 30 минут.
    """
    current_datetime = datetime.now()
    target_date = current_datetime.date()
    start_time = current_datetime.time()
    end_time = (datetime.combine(target_date, start_time) + timedelta(minutes=30)).time()

    # Загружаем комнаты из JSON
    all_rooms = [Room(**room) for room in load_rooms()]

    # Проверяем доступность каждой комнаты
    available_rooms = [
        room for room in all_rooms
        if check_room_availability(target_date, room.id, start_time, end_time)
    ]

    return available_rooms


@router.get("/bookings/user/", response_model=List[Booking])
async def get_user_bookings_endpoint(user_id: str, start_date: date, end_date: date):
    """
    Получить бронирования для конкретного пользователя.
    """
    bookings = get_user_bookings(user_id, start_date, end_date)
    return bookings