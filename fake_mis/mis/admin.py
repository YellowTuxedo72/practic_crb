from django.contrib import admin
from .models import (
    Patient,
    Doctor,
    DoctorSchedule,
    MedicalService,
    AppointmentSlot,
    Appointment,
    MedicalRecord,
)


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "record_type",
        "service",
        "date",
        "time",
        "doctor",
    )

    list_filter = (
        "record_type",
        "date",
    )

    search_fields = (
        "patient__last_name",
        "patient__first_name",
        "service__name",
    )

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_name",
        "first_name",
        "middle_name",
        "birth_date",
        "snils",
        "phone",
        "personal_data_consent_signed",
    )

    search_fields = (
        "last_name",
        "first_name",
        "snils",
        "phone",
    )
    
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_name",
        "first_name",
        "middle_name",
        "speciality",
    )

    search_fields = (
        "last_name",
        "first_name",
        "middle_name",
    )
    
@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "doctor",
        "weekday",
        "start_time",
        "end_time",
    )
    
@admin.register(MedicalService)
class MedicalServiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "price",
        "duration",
        "is_active",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "name",
    )
    
@admin.register(AppointmentSlot)
class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "service",
        "doctor",
        "date",
        "time",
        "is_available",
    )

    list_filter = (
        "service",
        "doctor",
        "date",
        "is_available",
    )

    search_fields = (
        "service__name",
        "doctor__last_name",
        "doctor__first_name",
    )
    
    
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "slot",
        "status",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "patient__last_name",
        "patient__first_name",
        "patient__snils",
    )