from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel

class Participant(BaseModel):
    id: str
    name: str
    telegram_id: Optional[str] = None

class Booking(BaseModel):
    id: str
    date: date
    start_time: time
    end_time: time
    room_id: str
    booked_by: Participant
    participants: List[Participant]
    status: str
    comment: Optional[str] = None

class Room(BaseModel):
    id: str
    name: str
    capacity: int
    features: List[str] = []
