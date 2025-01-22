from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel

class Participant(BaseModel):
    id: str  # ID пользователя
    name: str  # Имя пользователя
    nickname: Optional[str] = None  # Никнейм
    telegram_id: Optional[str] = None  # Telegram ID

class Booking(BaseModel):
    id: str  # Уникальный идентификатор бронирования
    date: date  # Дата бронирования
    start_time: time  # Время начала
    end_time: time  # Время окончания
    room_id: str  # ID комнаты
    booked_by: Participant  # Кто забронировал (объект)
    participants: List[Participant]  # Участники (объекты)
    status: str  # Статус бронирования (e.g., confirmed, pending)
    comment: Optional[str] = None  # Комментарий

class Room(BaseModel):
    id: str  # ID комнаты
    name: str  # Название
    capacity: int  # Вместимость
    features: List[str] = []  # Особенности комнаты
