from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel

class BookingCreate(BaseModel):
    date: date  # Только дата
    start_time: time  # Только время
    end_time: time  # Только время
    room_id: str
    participants: List[str]  # Список ID участников
    comment: Optional[str] = None

class BookingUpdate(BaseModel):
    start_time: Optional[time] = None  # Только время
    end_time: Optional[time] = None  # Только время
    room_id: Optional[str] = None
    participants: Optional[List[str]] = None
    comment: Optional[str] = None

class AvailabilityCheck(BaseModel):
    date: date  # Только дата
    start_time: time  # Только время
    end_time: time  # Только время
    min_capacity: Optional[int] = None
