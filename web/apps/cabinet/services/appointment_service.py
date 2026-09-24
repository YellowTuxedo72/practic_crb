from .mis_client import MISClient
from django.utils import timezone
from datetime import datetime

class AppointmentService:
    mis_client = MISClient()

    @staticmethod
    def get_services(category="consultation", parent_id=None):
        if parent_id is not None:
            return AppointmentService.mis_client.get_service_children(parent_id)

        return AppointmentService.mis_client.get_services(category)
    
    @staticmethod
    def get_available_slots(service_id):
        return AppointmentService.mis_client.get_service_slots(service_id)
    
    @staticmethod
    def get_slot(service_id, slot_id):
        slots = AppointmentService.get_available_slots(service_id)

        return next(
            (
                slot
                for slot in slots
                if str(slot["id"]) == str(slot_id)
            ),
            None,
        )
        
    @staticmethod
    def create_appointment(patient_id, slot_id):
        return AppointmentService.mis_client.create_appointment(patient_id, slot_id)
    
    @staticmethod
    def get_slots_for_date(service_id, selected_date):
        slots = AppointmentService.get_available_slots(service_id)

        return [
            slot
            for slot in slots
            if slot["date"].isoformat() == selected_date
        ]
    
    @staticmethod
    def get_service(service_id):
        return AppointmentService.mis_client.get_service(service_id)
    
    @staticmethod
    def select_slot(service_id, slot_id, selected_date):
        if not service_id:
            raise ValueError("Не удалось определить выбранную услугу.")

        if not slot_id:
            raise ValueError("Пожалуйста, выберите время.")

        if not selected_date:
            raise ValueError("Сначала выберите дату.")

        slots = AppointmentService.get_available_slots(service_id)

        selected_slot = next(
            (
                slot
                for slot in slots
                if str(slot["id"]) == str(slot_id)
                and slot["date"].isoformat() == selected_date
            ),
            None,
        )

        if selected_slot is None:
            raise ValueError("Выбранный слот больше недоступен.")

        return selected_slot
    
    @staticmethod
    def confirm_appointment(
        patient_id,
        slot_id,
    ):
        if not patient_id:
            raise ValueError(
                "Не удалось определить пациента."
            )

        if not slot_id:
            raise ValueError(
                "Не удалось определить выбранный слот."
            )

        return AppointmentService.create_appointment(
            patient_id,
            slot_id,
        )
    
    @staticmethod
    def clear_booking_session(request):
        for key in (
            "selected_service_id",
            "selected_slot_id",
            "appointment_step",
        ):
            request.session.pop(key, None)
            
  
    @staticmethod
    def get_nearest_appointment(patient_id):
        if not patient_id:
            return None

        appointments = (
            AppointmentService.mis_client
            .get_patient_appointments(patient_id)
        )

        if not appointments:
            return None

        now = timezone.localtime()
        future_appointments = []

        for appointment in appointments:
            if appointment["status"] != "scheduled":
                continue

            appointment_datetime = timezone.make_aware(
                datetime.combine(
                    appointment["date"],
                    appointment["time"],
                ),
                timezone.get_current_timezone(),
            )

            if appointment_datetime <= now:
                continue

            future_appointments.append(
                (
                    appointment_datetime,
                    appointment,
                )
            )

        if not future_appointments:
            return None

        return min(
            future_appointments,
            key=lambda item: item[0],
        )[1]
        
    @staticmethod
    def get_upcoming_appointments(patient_id):
        if not patient_id:
            return []

        appointments = AppointmentService.mis_client.get_patient_appointments(
            patient_id
        )

        if not appointments:
            return []

        now = timezone.localtime()
        upcoming = []

        for appointment in appointments:
            if appointment["status"] != "scheduled":
                continue

            appointment_datetime = timezone.make_aware(
                datetime.combine(
                    appointment["date"],
                    appointment["time"],
                ),
                timezone.get_current_timezone(),
            )

            if appointment_datetime <= now:
                continue

            upcoming.append(appointment)

        return sorted(
            upcoming,
            key=lambda appointment: (
                appointment["date"],
                appointment["time"],
            ),
        )
        
    @staticmethod
    def cancel_appointment(
        patient_id,
        appointment_id,
    ):
        if not patient_id:
            raise ValueError(
                "Не удалось определить пациента."
            )

        if not appointment_id:
            raise ValueError(
                "Не удалось определить запись."
            )

        return AppointmentService.mis_client.cancel_appointment(
            patient_id,
            appointment_id,
        )