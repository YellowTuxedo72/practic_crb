from datetime import date, time as datetime_time
from typing import Optional
from ninja import Schema
from decimal import Decimal


class PatientSearchSchema(Schema):
    snils: str
    phone: str
    birth_date: date


class PatientSearchOut(Schema):
    id: int
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date
    phone: str


class ServiceOut(Schema):
    id: int
    name: str
    has_children: bool
    price: Optional[float] = None


class SlotOut(Schema):
    id: int
    date: date
    time: datetime_time

class AppointmentCreate(Schema):
    patient_id: int
    slot_id: int


class AppointmentOut(Schema):
    id: int
    service: str
    doctor: str
    price: Decimal
    date: date
    time: datetime_time
    status: str


class MedicalRecordListOut(Schema):
    id: int
    type: str
    service: str
    date: date
    time: Optional[datetime_time] = None
    doctor: Optional[str] = None

class MedicalRecordOut(Schema):
    id: int
    type: str
    service: str
    date: date
    time: Optional[datetime_time] = None
    doctor: Optional[str] = None
    result: str
    conclusion: str
    protocol: str
    
class AppointmentCancelOut(Schema):
    id: int
    status: str
    
    
class MedicalRecordPageOut(Schema):
    items: list[MedicalRecordListOut]
    page: int
    page_size: int
    total: int
    pages: int