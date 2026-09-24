from .mis_client import MISClient


class MedicalRecordService:

    mis_client = MISClient()

    @staticmethod
    def get_patient_records(
        patient_id,
        page=1,
    ):
        if not patient_id:
            return None

        return MedicalRecordService.mis_client.get_patient_medical_records(
            patient_id,
            page,
        )
        
    @staticmethod
    def get_patient_record(
        patient_id,
        record_id,
    ):
        if not patient_id:
            raise ValueError(
                "Не удалось определить пациента."
            )

        if not record_id:
            raise ValueError(
                "Не удалось определить медицинскую запись."
            )

        return MedicalRecordService.mis_client.get_patient_medical_record(
            patient_id,
            record_id,
        )
    # @staticmethod
    # def get_patient_records(patient_id):
    #     if not patient_id:
    #         return None

    #     medical_data = MISService.get_patient_medical_records(patient_id)

    #     if not medical_data:
    #         return None

    #     months = {
    #         1: "января",
    #         2: "февраля",
    #         3: "марта",
    #         4: "апреля",
    #         5: "мая",
    #         6: "июня",
    #         7: "июля",
    #         8: "августа",
    #         9: "сентября",
    #         10: "октября",
    #         11: "ноября",
    #         12: "декабря",
    #     }

    #     for record in medical_data.get("records", []):

    #         if record.get("date"):
    #             try:
    #                 record["date"] = datetime.strptime(
    #                     record["date"],
    #                     "%Y-%m-%d"
    #                 ).date()

    #                 record["date_display"] = (
    #                     f"{record['date'].day} "
    #                     f"{months[record['date'].month]}"
    #                 )

    #             except (ValueError, TypeError):
    #                 pass

    #         if record.get("time"):
    #             try:
    #                 record["time"] = datetime.strptime(
    #                     record["time"],
    #                     "%H:%M:%S"
    #                 ).time()

    #                 record["time_display"] = record["time"].strftime("%H:%M")

    #             except (ValueError, TypeError):
    #                 pass

    #     return medical_data