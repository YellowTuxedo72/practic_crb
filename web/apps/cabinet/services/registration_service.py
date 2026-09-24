from .mis_client import (
    MISClient,
    MISNotFoundError,
    MISUnavailableError,
)
from .sms_service import SMSService
from cabinet.models import User


class RegistrationService:

    mis_client = MISClient()

    @staticmethod
    def start_registration(request, phone, snils, dob):
        try:
            patient_data = RegistrationService.mis_client.search_patient(
                snils=snils,
                phone=phone,
                birth_date=dob,
            )

        except MISNotFoundError:
            return False

        except MISUnavailableError:
            raise

        code = SMSService.generate_code()

        SMSService.send_sms(
            phone,
            code,
        )

        request.session["sms_code"] = code
        request.session["mis_patient_id"] = patient_data["id"]
        request.session["phone"] = phone

        request.session["first_name"] = patient_data.get(
            "first_name",
            "",
        )

        request.session["last_name"] = patient_data.get(
            "last_name",
            "",
        )

        request.session["patronymic"] = patient_data.get(
            "middle_name",
            "",
        )

        return True

    @staticmethod
    def verify_sms(request, entered_code):
        saved_code = request.session.get("sms_code")

        return entered_code == saved_code

    @staticmethod
    def get_phone(request):
        return request.session.get("phone")

    @staticmethod
    def get_test_code(request):
        return request.session.get("sms_code")

    @staticmethod
    def complete_registration(request, password):
        phone = request.session.get("phone")
        mis_patient_id = request.session.get("mis_patient_id")

        if not phone or not mis_patient_id:
            return None

        if User.objects.filter(phone=phone).exists():
            return False

        user = User.objects.create_user(
            phone=phone,
            password=password,
            mis_patient_id=mis_patient_id,
            first_name=request.session.get("first_name", ""),
            last_name=request.session.get("last_name", ""),
            patronymic=request.session.get("patronymic", ""),
        )

        RegistrationService.clear_session(request)

        return user

    @staticmethod
    def clear_session(request):
        for key in (
            "phone",
            "mis_patient_id",
            "sms_code",
            "reg_step",
            "first_name",
            "last_name",
            "patronymic",
        ):
            request.session.pop(key, None)