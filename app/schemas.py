from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel

class Participant(BaseModel):
    id: str
    name: str
    nickname: Optional[str] = None
    telegram_id: Optional[str] = None

class BookingCreate(BaseModel):
    date: date  # Дата бронирования
    start_time: time  # Время начала
    end_time: time  # Время окончания
    room_id: str  # Идентификатор комнаты
    booked_by: str  # ID бронирующего пользователя
    participants: List[str]  # Список ID участников
    comment: Optional[str] = None

class BookingUpdate(BaseModel):
    start_time: Optional[time] = None  # Время начала
    end_time: Optional[time] = None  # Время окончания
    room_id: Optional[str] = None  # Комната
    participants: Optional[List[str]] = None  # Участники
    comment: Optional[str] = None  # Комментарий

class AvailabilityCheck(BaseModel):
    date: date
    start_time: time
    end_time: time
    min_capacity: Optional[int] = None
    needed_interval: Optional[int] = 60  # 👈 Теперь это часть JSON

class Room(BaseModel):
    id: str  # ID комнаты
    name: str  # Название комнаты
    capacity: int  # Вместимость
    features: List[str] = []  # Список особенностей
