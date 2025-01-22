from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date, time
from app.schemas import BookingCreate, BookingUpdate
from app.models import Booking, Room, Participant
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
)
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# === Все бронирования

@router.get("/bookings/all")
async def get_all_bookings(
    start_date: Optional[date] = Query(None, description="Начальная дата бронирования"),
    end_date: Optional[date] = Query(None, description="Конечная дата бронирования"),
    rooms: Optional[str] = Query(None, description="Комнаты через запятую, например: '501,502'")
):
    """
    Получить все бронирования с фильтрацией.
    """
    try:
        bookings = get_bookings_in_range(
            start_date, 
            end_date, 
            rooms.split(",") if rooms else None
        )
        return bookings
    except Exception as e:
        logger.exception("Ошибка в маршруте /bookings/all")
        raise HTTPException(status_code=500, detail=str(e))

# === Основные маршруты для работы с бронированиями ===

@router.post("/bookings/create", response_model=Booking)
async def create_booking_endpoint(booking: BookingCreate):
    """
    Создать новое бронирование.
    """
    if not check_room_availability(booking.date, booking.room_id, booking.start_time, booking.end_time):
        raise HTTPException(status_code=400, detail="Room not available for selected time")

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


@router.get("/bookings/{booking_id}", response_model=Booking)
async def get_booking_endpoint(booking_id: str, target_date: str):
    """
    Получить бронирование по ID.
    """
    booking = get_booking(date.fromisoformat(target_date), booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.put("/bookings/{booking_id}/update", response_model=Booking)
async def update_booking_endpoint(
    booking_id: str,
    booking_update: BookingUpdate,
    target_date: str,
):
    """
    Обновить существующее бронирование.
    """
    target_date_obj = date.fromisoformat(target_date)
    bookings = read_bookings(target_date_obj)

    booking_index = next((i for i, b in enumerate(bookings) if b["id"] == booking_id), None)
    if booking_index is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    for key, value in booking_update.dict(exclude_unset=True).items():
        bookings[booking_index][key] = value

    write_bookings(target_date_obj, bookings)
    return bookings[booking_index]


@router.delete("/bookings/{booking_id}/delete")
async def delete_booking_endpoint(booking_id: str, target_date: str):
    """
    Удалить бронирование.
    """
    if not delete_booking(date.fromisoformat(target_date), booking_id):
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking deleted successfully"}
