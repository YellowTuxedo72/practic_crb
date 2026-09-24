import random


class SMSService:

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_sms(phone, code):

        print(
            f"[СМС ШЛЮЗ] Код {code} успешно отправлен на номер {phone}"
        )

        return True