from django.db import transaction
from django.shortcuts import get_object_or_404

from ninja import NinjaAPI
from ninja.errors import HttpError

from mis.models import (Patient, MedicalService, AppointmentSlot, Appointment)
from .schemas import (PatientSearchSchema, MedicalRecordPageOut, PatientSearchOut, ServiceOut, SlotOut, AppointmentCreate, AppointmentOut, AppointmentCancelOut, MedicalRecordOut)
from django.core.paginator import Paginator

api = NinjaAPI()


# Поиск пациента по снилсу, дате рождения и телефону
@api.post("/patients/search", response=PatientSearchOut)
def search_patient(request, data: PatientSearchSchema):
    patient = Patient.objects.filter(snils=data.snils, phone=data.phone, birth_date=data.birth_date).first()
    if not patient:
        raise HttpError(404, "Пациент не найден")
    return patient
    
@api.get("/services/{service_id}", response=ServiceOut)
def get_service(request, service_id: int):
    # Получаем только активную услугу.
    #
    # Если услуги не существует или она отключена,
    # возвращаем HTTP 404.
    service = get_object_or_404(MedicalService, id=service_id, is_active=True)

    return {
        "id": service.id,
        "name": service.name,
        "price": service.price,
        "has_children": service.children.filter(is_active=True).exists(),
    }
    
@api.get("/services", response=list[ServiceOut])
def get_services(request, category: str):
    services = (MedicalService.objects.filter(category=category, parent=None, is_active=True).order_by("name"))

    return [
        {
            "id": service.id,
            "name": service.name,
            "price": service.price,
            "has_children": service.children.filter(is_active=True).exists(),
        }
        for service in services
    ]
    
@api.get("/services/{service_id}/children", response=list[ServiceOut])
def get_service_children(request, service_id: int):
    # Сначала проверяем, что родительская услуга
    # существует и активна.
    service = get_object_or_404(MedicalService, id=service_id, is_active=True)

    # Получаем только активные дочерние услуги.
    children = (service.children.filter(is_active=True).order_by("name"))

    return [
        {
            "id": child.id,
            "name": child.name,
            "price": child.price,
            "has_children": child.children.filter(is_active=True).exists(),
        }
        for child in children
    ]
    
    
@api.get("/services/{service_id}/slots", response=list[SlotOut],)
def get_service_slots(request, service_id: int):
    # Проверяем, что услуга существует и активна.
    service = get_object_or_404(MedicalService, id=service_id, is_active=True)

    # Получаем только свободные слоты этой услуги.
    slots = (AppointmentSlot.objects.filter(service=service, is_available=True).select_related("doctor").order_by("date", "time"))

    return slots

# Создание записи
@api.post("/appointments", response=AppointmentOut)
def create_appointment(request, data: AppointmentCreate):
    patient = get_object_or_404(Patient, id=data.patient_id)

    with transaction.atomic():
        slot = (AppointmentSlot.objects.select_for_update().select_related("service","doctor").filter(id=data.slot_id).first())
        if slot is None:
            raise HttpError(404, "Слот не найден")

        if not slot.is_available:
            raise HttpError(409, "Выбранное время уже занято.")
        
        active_appointment = Appointment.objects.filter(
            slot=slot,
            status="scheduled",
        ).exists()

        if active_appointment:
            raise HttpError(
                409,
                "Выбранное время уже занято.",
            )

        if not slot.service.is_active:
            raise HttpError(409, "Выбранная медицинская услуга недоступна.")

        if not slot.doctor.services.filter(id=slot.service_id).exists():
            raise HttpError(409, "Выбранный врач не оказывает данную медицинскую услугу.")
        
        appointment = Appointment.objects.create(patient=patient, slot=slot, status="scheduled")

        # Слот больше нельзя выбрать повторно,
        # поэтому помечаем его как занятый.
        # update_fields ограничивает UPDATE только этим полем.
        slot.is_available = False
        slot.save(update_fields=["is_available"])

    return {
        "id": appointment.id,
        "service": slot.service.name,
        "doctor": (
            f"{slot.doctor.last_name} "
            f"{slot.doctor.first_name} "
            f"{slot.doctor.middle_name or ''}"
        ).strip(),
        "price": slot.service.price,
        "date": slot.date,
        "time": slot.time,
        "status": appointment.status,
    }


# Отмена записи пациента
@api.patch("/patients/{patient_id}/appointments/{appointment_id}/cancel", response=AppointmentCancelOut)
def cancel_appointment(
    request,
    patient_id: int,
    appointment_id: int,
):
    with transaction.atomic():

        # Ищем запись не только по её ID,
        # но и проверяем, что она принадлежит указанному пациенту.
        appointment = (
            Appointment.objects
            .select_for_update()
            .select_related("slot")
            .filter(
                id=appointment_id,
                patient_id=patient_id,
            )
            .first()
        )

        # Если записи нет или она принадлежит другому пациенту,
        # наружу не раскрываем существование чужой записи.
        if appointment is None:
            raise HttpError(
                404,
                "Запись пациента не найдена.",
            )

        # Повторно отменять уже отменённую запись нельзя.
        if appointment.status == "cancelled":
            raise HttpError(
                409,
                "Запись уже отменена.",
            )

        # Меняем статус записи.
        appointment.status = "cancelled"
        appointment.save(update_fields=["status"])

        # Освобождаем связанный слот.
        slot = appointment.slot
        slot.is_available = True
        slot.save(update_fields=["is_available"])

    return {
        "id": appointment.id,
        "status": appointment.status,
    }

# 
@api.get(
    "/patients/{patient_id}/appointments",
    response=list[AppointmentOut],
)
def get_patient_appointments(
    request,
    patient_id: int,
):
    patient = get_object_or_404(
        Patient,
        id=patient_id,
    )

    if not patient.personal_data_consent_signed:
        raise HttpError(
            403,
            "Доступ к данным о записях запрещён.",
        )

    appointments = (
        Appointment.objects
        .filter(patient=patient)
        .select_related(
            "slot__service",
            "slot__doctor",
        )
        .order_by(
            "slot__date",
            "slot__time",
        )
    )

    return [
        {
            "id": appointment.id,
            "service": appointment.slot.service.name,
            "doctor": (
                f"{appointment.slot.doctor.last_name} "
                f"{appointment.slot.doctor.first_name} "
                f"{appointment.slot.doctor.middle_name or ''}"
            ).strip(),
            "price": appointment.slot.service.price,
            "date": appointment.slot.date,
            "time": appointment.slot.time,
            "status": appointment.status,
        }
        for appointment in appointments
    ]

@api.get(
    "/patients/{patient_id}/medical-records",
    response=MedicalRecordPageOut,
)
def get_patient_medical_records(
    request,
    patient_id: int,
    page: int = 1,
):
    patient = get_object_or_404(
        Patient,
        id=patient_id,
    )

    if not patient.personal_data_consent_signed:
        raise HttpError(
            403,
            "Доступ к медицинским данным запрещён.",
        )

    records = patient.medical_records.select_related(
        "service",
        "doctor",
    ).order_by(
        "-date",
        "-time",
    )

    paginator = Paginator(
        records,
        10,
    )

    page_obj = paginator.get_page(page)

    return {
        "items": [
            {
                "id": record.id,
                "type": record.record_type,
                "service": record.service.name,
                "date": record.date,
                "time": record.time,
                "doctor": (
                    f"{record.doctor.last_name} "
                    f"{record.doctor.first_name} "
                    f"{record.doctor.middle_name or ''}"
                ).strip()
                if record.doctor
                else None,
            }
            for record in page_obj.object_list
        ],
        "page": page_obj.number,
        "pages": paginator.num_pages,
        "page_size": 10,
        "total": paginator.count,
    }
    
@api.get(
    "/patients/{patient_id}/medical-records/{record_id}",
    response=MedicalRecordOut,
)
def get_patient_medical_record(
    request,
    patient_id: int,
    record_id: int,
):
    patient = get_object_or_404(
        Patient,
        id=patient_id,
    )

    if not patient.personal_data_consent_signed:
        raise HttpError(
            403,
            "Доступ к медицинским данным запрещён.",
        )

    record = get_object_or_404(
        patient.medical_records.select_related(
            "service",
            "doctor",
        ),
        id=record_id,
    )

    return {
        "id": record.id,
        "type": record.record_type,
        "service": record.service.name,
        "date": record.date,
        "time": record.time,
        "doctor": (
            f"{record.doctor.last_name} "
            f"{record.doctor.first_name} "
            f"{record.doctor.middle_name or ''}"
        ).strip()
        if record.doctor
        else None,
        "result": record.result,
        "conclusion": record.conclusion,
        "protocol": record.protocol,
    }