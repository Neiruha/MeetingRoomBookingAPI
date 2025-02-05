from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date, time
from app.schemas import BookingCreate, BookingUpdate, Room, Participant
from app.models import Booking
from app.database import (
    create_booking,
    get_booking,
    delete_booking,
    check_room_availability,
    read_bookings,
    write_bookings,
    load_rooms,
    save_rooms,
    load_users,
    save_users,
    get_bookings_in_range,
    add_user, 
    find_available_time_slots, 
    is_user_booked
)

router = APIRouter()

# === 1. Получение всех бронирований с фильтрацией ===

@router.get("/bookings/all")
async def get_all_bookings(
    start_date: Optional[date] = Query(None, description="Начальная дата бронирования"),
    end_date: Optional[date] = Query(None, description="Конечная дата бронирования"),
    rooms: Optional[str] = Query(None, description="Комнаты через запятую, например: '501,502'")
):
    """
    Получить все бронирования с фильтрацией по датам и комнатам.
    """
    try:
        room_ids = rooms.split(",") if rooms else None
        bookings = get_bookings_in_range(start_date, end_date, room_ids)
        return bookings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === 2. Создание нового бронирования ===

@router.post("/bookings/create", response_model=Booking)
async def create_booking_endpoint(booking: BookingCreate):
    """
    Создать новое бронирование.
    """

    target_date = booking.date
    start_time = booking.start_time
    end_time = booking.end_time

    # 1️⃣ Проверяем, свободна ли комната
    if not check_room_availability(target_date, booking.room_id, start_time, end_time):
        available_slots = find_available_time_slots(target_date, booking.room_id)
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Комната недоступна в указанное время.",
                "available_slots": available_slots
            }
        )

    # 2️⃣ Проверяем, свободны ли все участники
    for participant_id in booking.participants:
        if is_user_booked(target_date, participant_id, start_time, end_time):
            raise HTTPException(
                status_code=422,
                detail={
                    "message": f"Участник {participant_id} уже записан на это время.",
                    "conflicting_participant": participant_id
                }
            )

    # 3️⃣ Создаем бронирование
    new_booking = create_booking({
        "id": f"{booking.room_id}{booking.date.strftime('%Y%m%d')}{booking.start_time.strftime('%H%M')}",
        "room_id": booking.room_id,
        "date": booking.date.strftime('%Y-%m-%d'),
        "start_time": booking.start_time.strftime('%H:%M'),
        "end_time": booking.end_time.strftime('%H:%M'),
        "booked_by": booking.booked_by,
        "participants": booking.participants,
        "comment": booking.comment or "",
        "status": "confirmed",
    })
    
    return new_booking

# === 3. Получение бронирования по ID ===

@router.get("/bookings/{booking_id}", response_model=Booking)
async def get_booking_endpoint(booking_id: str, target_date: date):
    """
    Получить бронирование по ID.
    """
    booking = get_booking(target_date, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    return booking

# === 4. Добавление новой комнаты ===

@router.post("/rooms/add")
async def add_room(room: Room):
    """
    Добавить новую комнату.
    """
    rooms = load_rooms()
    if any(r["id"] == room.id for r in rooms):
        raise HTTPException(status_code=400, detail="Комната уже существует")
    rooms.append(room.dict())
    save_rooms(rooms)
    return {"message": f"Комната {room.id} успешно добавлена"}

# === 5. Получение всех комнат ===

@router.get("/rooms/all", response_model=List[Room])
async def get_all_rooms():
    """
    Получить список всех комнат.
    """
    return load_rooms()

# === 6. Добавление нового пользователя ===

@router.post("/users/add")
async def add_user_endpoint(user: Participant):
    """
    Добавить нового пользователя.
    """
    users = load_users()
    if user.id in users:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    users[user.id] = {"name": user.name, "nickname": user.telegram_id or ""}
    save_users(users)
    return {"message": f"Пользователь {user.id} успешно добавлен"}

# === 7. Получение всех пользователей ===

@router.get("/users/all", response_model=List[Participant])
async def get_all_users():
    """
    Получить список всех пользователей.
    """
    users = load_users()
    return [Participant(id=user_id, name=data["name"], telegram_id=data.get("nickname")) for user_id, data in users.items()]


@router.get("/bookings/user/", response_model=List[Booking])
async def get_user_bookings_endpoint(user_id: str, start_date: date, end_date: date):
    """
    Получить бронирования для конкретного пользователя.
    """
    bookings = get_user_bookings(user_id, start_date, end_date)
    return bookings