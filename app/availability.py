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



def generate_time_slots(start: time, end: time, interval: int) -> List[tuple]:
    """
    Разбивает заданный временной промежуток на интервалы по interval минут.
    """
    slots = []
    current = datetime.combine(date.today(), start)
    end_dt = datetime.combine(date.today(), end)

    while current + timedelta(minutes=interval) <= end_dt:
        slots.append((current.time(), (current + timedelta(minutes=interval)).time()))
        current += timedelta(minutes=interval)

    return slots


@router.post("/plan/")
async def plan_availability_endpoint(check: AvailabilityCheck):
    """
    Возвращает список доступных временных слотов в переговорных, деля день на интервалы.
    """
    target_date = check.date
    start_time = check.start_time
    end_time = check.end_time
    needed_interval = check.needed_interval  # Теперь это часть JSON!

    # Загружаем комнаты
    all_rooms = [Room(**room) for room in load_rooms()]

    # Получаем список всех возможных слотов в рамках рабочего дня
    all_slots = generate_time_slots(start_time, end_time, needed_interval)

    # Отфильтруем только свободные слоты для каждой комнаты
    plan = []

    for room in all_rooms:
        busy_slots = []

        # Проверяем, какие слоты уже заняты
        for slot_start, slot_end in all_slots:
            if not check_room_availability(target_date, room.id, slot_start, slot_end):
                busy_slots.append((slot_start, slot_end))

        # Оставшиеся слоты считаем свободными
        free_slots = [slot for slot in all_slots if slot not in busy_slots]

        # Если нет свободных мест, ищем соседние доступные интервалы
        if not free_slots:
            shifted_slots = []
            search_direction = [-1, 1]  # Сначала назад, потом вперед
            for direction in search_direction:
                shift = 1
                while shift <= 3:  # Проверим три ближайших интервала в обе стороны
                    shifted_start = (datetime.combine(date.today(), start_time) + timedelta(minutes=needed_interval * direction * shift)).time()
                    shifted_end = (datetime.combine(date.today(), end_time) + timedelta(minutes=needed_interval * direction * shift)).time()
                    
                    if check_room_availability(target_date, room.id, shifted_start, shifted_end):
                        shifted_slots.append((shifted_start, shifted_end))
                        break  # Нашли ближайший слот — дальше не идем
                    shift += 1

            if shifted_slots:
                plan.append({
                    "room_id": room.id,
                    "room_name": room.name,
                    "alternative_slots": shifted_slots
                })

        else:
            plan.append({
                "room_id": room.id,
                "room_name": room.name,
                "available_slots": free_slots
            })

    return plan
