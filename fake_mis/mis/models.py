from django.db import models


class Patient(models.Model):
    
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    birth_date = models.DateField(verbose_name="Дата рождения")
    snils = models.CharField(max_length=14, unique=True, verbose_name="СНИЛС")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    personal_data_consent_signed = models.BooleanField(
        default=False,
        verbose_name="Согласие на обработку ПД подписано очно"
    )

    personal_data_consent_signed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата подписания согласия"
    )

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"


    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Doctor(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    speciality = models.CharField(max_length=100, verbose_name="Специальность")
    services = models.ManyToManyField(
        "MedicalService",
        blank=True,
        related_name="doctors",
        verbose_name="Оказываемые услуги"
    )

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"


    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    
class DoctorSchedule(models.Model):
    WEEKDAYS = [
        (0, "Понедельник"),
        (1, "Вторник"),
        (2, "Среда"),
        (3, "Четверг"),
        (4, "Пятница"),
        (5, "Суббота"),
        (6, "Воскресенье"),
    ]

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name="Врач"
    )

    weekday = models.IntegerField(
        choices=WEEKDAYS,
        verbose_name="День недели"
    )

    start_time = models.TimeField(
        verbose_name="Начало работы"
    )

    end_time = models.TimeField(
        verbose_name="Конец работы"
    )


    class Meta:
        verbose_name = "Расписание врача"
        verbose_name_plural = "Расписание врачей"


    def __str__(self):
        return (
            f"{self.doctor} - "
            f"{self.get_weekday_display()} "
            f"{self.start_time}-{self.end_time}"
        )
        
        
class MedicalService(models.Model):

    CATEGORY_CHOICES = [
        ("consultation", "Консультации специалистов"),
        ("analysis", "Анализы"),
        ("diagnostic", "Диагностика"),
        ("procedure", "Процедуры"),
        ("dentistry", "Стоматология"),
        ("rehabilitation", "Реабилитация"),
    ]

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name="Категория"
    )

    name = models.CharField(
        max_length=200,
        verbose_name="Название услуги"
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        verbose_name="Родительская услуга"
    )

    duration = models.PositiveIntegerField(
        default=30,
        verbose_name="Длительность (минуты)"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Стоимость"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Доступна"
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Справочник услуг"

    def __str__(self):
        return self.name
    
    
class AppointmentSlot(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="slots",
        verbose_name="Врач"
    )

    service = models.ForeignKey(
        MedicalService,
        on_delete=models.CASCADE,
        related_name="slots",
        verbose_name="Услуга"
    )

    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")

    is_available = models.BooleanField(
        default=True,
        verbose_name="Свободен"
    )

    class Meta:
        ordering = ["date", "time"]

    def __str__(self):
        return f"{self.service} — {self.date} {self.time}"
    
    
class Appointment(models.Model):

    STATUS_CHOICES = [
        ("scheduled", "Запланирована"),
        ("completed", "Завершена"),
        ("cancelled", "Отменена"),
        ("no_show", "Не явился"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    slot = models.ForeignKey(
        AppointmentSlot,
        on_delete=models.PROTECT,
        related_name="appointments",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient} - {self.slot}"
    
class MedicalRecord(models.Model):

    TYPE_CHOICES = [
        ("analysis", "Анализ"),
        ("research", "Исследование"),
        ("visit_protocol", "Протокол приёма"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="medical_records",
        verbose_name="Пациент"
    )

    service = models.ForeignKey(
        MedicalService,
        on_delete=models.PROTECT,
        related_name="medical_records",
        verbose_name="Услуга"
    )

    record_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        verbose_name="Тип записи"
    )

    date = models.DateField(
        verbose_name="Дата"
    )

    time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Время"
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="medical_records",
        verbose_name="Врач"
    )

    result = models.TextField(
        blank=True,
        verbose_name="Результат"
    )

    conclusion = models.TextField(
        blank=True,
        verbose_name="Заключение"
    )

    protocol = models.TextField(
        blank=True,
        verbose_name="Протокол"
    )