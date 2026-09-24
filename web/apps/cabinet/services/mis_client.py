import requests
from datetime import date, time
from django.conf import settings


class MISClientError(Exception):
    """Базовая ошибка интеграции с МИС."""


class MISUnavailableError(MISClientError):
    """МИС недоступна или не отвечает."""


class MISNotFoundError(MISClientError):
    """Запрашиваемый ресурс не найден."""


class MISConflictError(MISClientError):
    """МИС отклонила операцию из-за конфликта состояния."""


class MISPermissionError(MISClientError):
    """Недостаточно прав для доступа к данным МИС."""


class MISClient:
    """
    HTTP-клиент для взаимодействия с API МИС.
    """

    def __init__(self):
        self.base_url = settings.MIS_BASE_URL
        self.timeout = settings.MIS_TIMEOUT

    def _request(
        self,
        method,
        path,
        *,
        params=None,
        json=None,
    ):
        try:
            response = requests.request(
                method=method,
                url=f"{self.base_url}{path}",
                params=params,
                json=json,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise MISUnavailableError(
                "МИС временно недоступна."
            ) from exc

        if response.status_code == 404:
            raise MISNotFoundError(
                "Запрашиваемый ресурс МИС не найден."
            )

        if response.status_code == 403:
            raise MISPermissionError(
                "Доступ к данным МИС запрещён."
            )

        if response.status_code == 409:
            try:
                error_data = response.json()
                message = error_data.get(
                    "detail",
                    "Операция не может быть выполнена.",
                )
            except ValueError:
                message = (
                    "Операция не может быть выполнена."
                )

            raise MISConflictError(message)

        if not 200 <= response.status_code < 300:
            try:
                error_data = response.json()
            except ValueError:
                error_data = response.text

            raise MISClientError(
                f"МИС вернула ошибку HTTP {response.status_code}: "
                f"{error_data}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise MISClientError(
                "МИС вернула некорректный JSON."
            ) from exc

    def search_patient(
        self,
        snils,
        phone,
        birth_date,
    ):
        return self._request(
            "POST",
            "/patients/search",
            json={
                "snils": snils,
                "phone": phone,
                "birth_date": str(birth_date),
            },
        )

    def get_services(
        self,
        category="consultation",
    ):
        return self._request(
            "GET",
            "/services",
            params={
                "category": category,
            },
        )

    def get_service_children(
        self,
        service_id,
    ):
        return self._request(
            "GET",
            f"/services/{service_id}/children",
        )

    def get_service(
        self,
        service_id,
    ):
        return self._request(
            "GET",
            f"/services/{service_id}",
        )

    def get_service_slots(
        self,
        service_id,
    ):
        slots = self._request(
            "GET",
            f"/services/{service_id}/slots",
        )

        for slot in slots:
            if isinstance(slot.get("date"), str):
                slot["date"] = date.fromisoformat(
                    slot["date"]
                )

            if isinstance(slot.get("time"), str):
                slot["time"] = time.fromisoformat(
                    slot["time"]
                )

        return slots

    def create_appointment(
        self,
        patient_id,
        slot_id,
    ):
        appointment = self._request(
            "POST",
            "/appointments",
            json={
                "patient_id": patient_id,
                "slot_id": slot_id,
            },
        )

        if isinstance(appointment.get("date"), str):
            appointment["date"] = date.fromisoformat(
                appointment["date"]
            )

        if isinstance(appointment.get("time"), str):
            appointment["time"] = time.fromisoformat(
                appointment["time"]
            )

        return appointment

    def get_patient_appointments(
        self,
        patient_id,
    ):
        appointments = self._request(
            "GET",
            f"/patients/{patient_id}/appointments",
        )

        for appointment in appointments:
            if isinstance(appointment.get("date"), str):
                appointment["date"] = date.fromisoformat(
                    appointment["date"]
                )

            if isinstance(appointment.get("time"), str):
                appointment["time"] = time.fromisoformat(
                    appointment["time"]
                )

        return appointments

    def get_patient_medical_records(
        self,
        patient_id,
        page=1,
    ):
        data = self._request(
            "GET",
            f"/patients/{patient_id}/medical-records",
            params={
                "page": page,
            },
        )

        for record in data["items"]:
            if isinstance(record.get("date"), str):
                record["date"] = date.fromisoformat(
                    record["date"]
                )

            if isinstance(record.get("time"), str):
                record["time"] = time.fromisoformat(
                    record["time"]
                )

        return data

    def get_patient_medical_record(
        self,
        patient_id,
        record_id,
    ):
        record = self._request(
            "GET",
            f"/patients/{patient_id}/medical-records/{record_id}",
        )

        if isinstance(record.get("date"), str):
            record["date"] = date.fromisoformat(
                record["date"]
            )

        if isinstance(record.get("time"), str):
            record["time"] = time.fromisoformat(
                record["time"]
            )

        return record

    def cancel_appointment(
        self,
        patient_id,
        appointment_id,
    ):
        return self._request(
            "PATCH",
            f"/patients/{patient_id}/appointments/{appointment_id}/cancel",
        )