import requests


class MISService:
    """Сервис интеграции с МИС поликлиники."""

    MIS_BASE_URL = "http://127.0.0.1:9000/api"

    @staticmethod
    def check_patient_exists(snils, phone, dob):
        try:
            response = requests.post(
                f"{MISService.MIS_BASE_URL}/patient/search",
                json={
                    "snils": snils,
                    "phone": phone,
                    "birth_date": str(dob),
                },
                timeout=5,
            )

            if response.status_code != 200:
                return None

            try:
                patient = response.json()
            except ValueError:
                return None

            if "id" not in patient:
                return None

            return patient

        except requests.exceptions.RequestException:
            return None
        
    @staticmethod
    def get_services(category="consultation", parent_id=None):
        try:
            if parent_id:
                response = requests.get(f"{MISService.MIS_BASE_URL}/services/{parent_id}/children", timeout=5)
            else:
                response = requests.get(f"{MISService.MIS_BASE_URL}/services", params={"category": category}, timeout=5)

            if response.status_code != 200:
                return None

            return response.json()

        except requests.exceptions.RequestException:
            return None
        except ValueError:
            return None
        
    @staticmethod
    def get_service_slots(service_id):
        try:
            response = requests.get(f"{MISService.MIS_BASE_URL}/services/{service_id}/slots", timeout=5)

            if response.status_code != 200:
                return None

            try:
                return response.json()
            except ValueError:
                return None

        except requests.exceptions.RequestException:
            return None
        
    # @staticmethod
    # def get_service(service_id):
    #     try:
    #         response = requests.get(f"{MISService.MIS_BASE_URL}/services/{service_id}", timeout=5)

    #         if response.status_code != 200:
    #             return None

    #         try:
    #             return response.json()
    #         except ValueError:
    #             return None

    #     except requests.exceptions.RequestException:
    #         return None

    # @staticmethod
    # def get_slot(slot_id):
    #     try:
    #         response = requests.get(f"{MISService.MIS_BASE_URL}/slots/{slot_id}", timeout=5)

    #         if response.status_code != 200:
    #             return None

    #         try:
    #             return response.json()
    #         except ValueError:
    #             return None

    #     except requests.exceptions.RequestException:
    #         return None
    
    @staticmethod
    def create_appointment(patient_id, slot_id):
        try:
            response = requests.post(
                f"{MISService.MIS_BASE_URL}/appointments",
                json={"patient_id": patient_id, "slot_id": slot_id},
                timeout=5,
            )

            if response.status_code not in (200, 201):
                return None

            try:
                return response.json()
            except ValueError:
                return None

        except requests.exceptions.RequestException:
            return None
        
    @staticmethod
    def get_service(service_id):
        try:
            response = requests.get(f"{MISService.MIS_BASE_URL}/services/{service_id}", timeout=5)

            if response.status_code != 200:
                return None

            try:
                return response.json()
            except ValueError:
                return None

        except requests.exceptions.RequestException:
            return None
        
    

    @staticmethod
    def get_patient_appointments(patient_id):
        try:
            response = requests.get(
                f"{MISService.MIS_BASE_URL}/patients/{patient_id}/appointments",
                timeout=5,
            )

            if response.status_code != 200:
                return None

            try:
                return response.json()
            except ValueError:
                return None

        except requests.exceptions.RequestException:
            return None
        
    @staticmethod
    def get_patient_medical_records(patient_id):
        try:
            response = requests.get(
                f"{MISService.MIS_BASE_URL}/patients/{patient_id}/medical-records",
                timeout=5
            )

            if response.status_code != 200:
                return None

            try:
                return response.json()
            except ValueError:
                return None

        except requests.exceptions.RequestException:
            return None