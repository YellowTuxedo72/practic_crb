from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class SimpleUserManager(BaseUserManager):
    """Менеджер, который вообще ничего не знает про username"""
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Телефон обязателен')
        
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Идеальная модель для авторизации строго по Телефону + Паролю"""
    phone = models.CharField(max_length=15, unique=True, verbose_name="Номер телефона")
    mis_patient_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="ID пациента в МИС")
    
    # ХРАНИМ ПОЛНОЕ ФИО ПАЦИЕНТА
    last_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Фамилия")
    first_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Имя")
    patronymic = models.CharField(max_length=150, blank=True, null=True, verbose_name="Отчество")
    
    # Минимальный набор полей для работы админки Django
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Дата регистрации")

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = SimpleUserManager()

    # Свойство для компактного вывода "Фамилия И." в хедере
    @property
    def short_name(self):
        if self.last_name and self.first_name:
            # Срез [:1] берет только первую букву имени
            return f"{self.last_name} {self.first_name[:1]}."
        return self.phone

    # Свойство для вывода полного ФИО внутри личного кабинета (если понадобится)
    @property
    def get_full_fio(self):
        if self.last_name and self.first_name:
            p = self.patronymic if self.patronymic else ""
            return f"{self.last_name} {self.first_name} {p}".strip()
        return self.phone

    def __str__(self):
        return self.get_full_fio
