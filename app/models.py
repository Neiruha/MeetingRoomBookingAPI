from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel

class Participant(BaseModel):
    id: str  # ID ������������
    name: str  # ��� ������������
    nickname: Optional[str] = None  # �������
    telegram_id: Optional[str] = None  # Telegram ID

class Booking(BaseModel):
    id: str  # ���������� ������������� ������������
    date: date  # ���� ������������
    start_time: time  # ����� ������
    end_time: time  # ����� ���������
    room_id: str  # ID �������
    booked_by: Participant  # ��� ������������ (������)
    participants: List[Participant]  # ��������� (�������)
    status: str  # ������ ������������ (e.g., confirmed, pending)
    comment: Optional[str] = None  # �����������

class Room(BaseModel):
    id: str  # ID �������
    name: str  # ��������
    capacity: int  # �����������
    features: List[str] = []  # ����������� �������
