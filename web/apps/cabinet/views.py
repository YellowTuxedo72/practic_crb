from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import User
from .forms import RegistrationForm, UserLoginForm
from .utils import format_phone
from .services.registration_service import RegistrationService
from django.contrib.auth.decorators import login_required
from .services.appointment_service import AppointmentService
from .services.medical_record_service import MedicalRecordService
from .services.mis_client import (
    MISConflictError,
    MISNotFoundError,
    MISUnavailableError, MISPermissionError,
)
from datetime import date, time
from django.http import JsonResponse


def register_view(request):
    # Уже авторизованный пользователь
    if request.user.is_authenticated:
        return redirect("website:index")

    current_step = request.session.get("reg_step", "step_1")

    if request.method == "POST":

        # ШАГ 1 — поиск пациента в МИС
        if current_step == "step_1":
            form = RegistrationForm(request.POST)

            if form.is_valid():
                try:
                    success = RegistrationService.start_registration(
                        request,
                        form.cleaned_data["phone"],
                        form.cleaned_data["snils"],
                        form.cleaned_data["dob"],
                    )

                except MISUnavailableError:
                    messages.error(
                        request,
                        "Система МИС временно недоступна. Попробуйте позже.",
                    )
                else:
                    if success:
                        request.session["reg_step"] = "step_2"
                        return redirect("cabinet:register")

                    messages.error(
                        request,
                        "Пациент не найден в базе поликлиники.",
                    )

            else:
                for error in form.errors.values():
                    messages.error(request, error[0])

        # ШАГ 2 — проверка SMS
        elif current_step == "step_2":
            entered_code = request.POST.get("sms_code")

            if RegistrationService.verify_sms(
                request,
                entered_code
            ):
                request.session["reg_step"] = "step_3"
                return redirect("cabinet:register")

            messages.error(
                request,
                "Неверный код подтверждения."
            )

        # ШАГ 3 — создание аккаунта
        elif current_step == "step_3":
            password = request.POST.get("password")
            password_confirm = request.POST.get("password_confirm")

            if password != password_confirm:
                messages.error(
                    request,
                    "Пароли не совпадают."
                )

            elif len(password) < 8:
                messages.error(
                    request,
                    "Пароль должен содержать минимум 8 символов."
                )

            else:
                user = RegistrationService.complete_registration(
                    request,
                    password
                )

                if user is None:
                    messages.error(
                        request,
                        "Сессия регистрации истекла."
                    )
                    RegistrationService.clear_session(request)
                    return redirect("cabinet:register")

                if user is False:
                    messages.error(
                        request,
                        "Аккаунт с таким номером телефона уже существует."
                    )
                    RegistrationService.clear_session(request)
                    return redirect("cabinet:login")

                login(request, user)
                return redirect("website:index")

    # РЕНДЕРИНГ ТЕКУЩЕГО ШАГА

    if current_step == "step_1":
        return render(
            request,
            "cabinet/register.html"
        )

    if current_step == "step_2":
        return render(
            request,
            "cabinet/verify_phone.html",
            {
                "phone": format_phone(
                    RegistrationService.get_phone(request)
                ),
                "test_code": RegistrationService.get_test_code(request),
            }
        )

    if current_step == "step_3":
        return render(
            request,
            "cabinet/create_password.html"
        )

    # Если в сессии оказался неизвестный шаг
    RegistrationService.clear_session(request)
    return redirect("cabinet:register")

def logout_view(request):
    logout(request)  # Полностью очищает сессию и разлогинивает
    return redirect("website:index") 

def login_view(request):
    # Если пользователь уже авторизован, уводим его на главную
    if request.user.is_authenticated:
        return redirect("website:index")

    # Инициализируем пустую форму для GET-запроса
    form = UserLoginForm()

    if request.method == "POST":
        # Передаем POST-данные в нашу форму
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            # Извлекаем очищенные данные из полей формы
            username = form.cleaned_data["username"]  # Приходит: "+7 (999) 123-45-67"
            password = form.cleaned_data["password"]
            remember_me = form.cleaned_data["remember_me"]

            # ИСПРАВЛЕНИЕ 1: Удаляем маску, оставляя только цифры (станет: "79991234567")
            clean_phone = "".join(filter(str.isdigit, username))


            # Аутентифицируем пользователя в Django по очищенному номеру
            user = authenticate(request, username=clean_phone, password=password)

            if user is not None:
                # Настройка времени жизни сессии ("Запомнить меня")
                if remember_me:
                    request.session.set_expiry(None)  # Стандартные 2 недели
                else:
                    request.session.set_expiry(0)     # Удалить при закрытии браузера

                # Логиним пользователя
                login(request, user)
                return redirect("website:index")
            else:
                print('Неверный номер телефона или пароль.')
                messages.error(request, "Неверный номер телефона или пароль.")
        else:
            # Если форма не валидна (например, телефон не прошел базовую проверку)
            for error in form.errors.values():
                messages.error(request, error[0])
                
    # ИСПРАВЛЕНИЕ 2: Обязательно передаем форму в контекст шаблона
    return render(request, "cabinet/login.html", {"form": form})


@login_required(login_url="cabinet:login")
def patient_cabinet_view(request):

    patient_id = request.user.mis_patient_id

    # =====================================================
    # БЛИЖАЙШИЕ И БУДУЩИЕ ЗАПИСИ
    # =====================================================

    try:
        nearest_appointment = (
            AppointmentService.get_nearest_appointment(
                patient_id
            )
        )

        upcoming_appointments = (
            AppointmentService.get_upcoming_appointments(
                patient_id
            )
        )

        appointments_available = True
        appointments_message = None

    except MISPermissionError:
        nearest_appointment = None
        upcoming_appointments = []

        appointments_available = False

        appointments_message = (
            "Для просмотра сведений о предстоящих "
            "записях необходимо предоставить согласие "
            "на обработку персональных данных."
        )

    except MISUnavailableError:
        nearest_appointment = None
        upcoming_appointments = []

        appointments_available = False

        appointments_message = (
            "Система МИС временно недоступна. "
            "Попробуйте позже."
        )
    # Текущая страница медицинской истории
    try:
        page = int(request.GET.get("page", 1))
    except (TypeError, ValueError):
        page = 1

    try:
        medical_data = MedicalRecordService.get_patient_records(
            patient_id,
            page=page,
        )

        medical_data["available"] = True

    except MISPermissionError:
        medical_data = {
            "available": False,
            "items": [],
            "page": 1,
            "pages": 1,
            "page_size": 10,
            "total": 0,
            "message": (
                "Медицинские данные недоступны до очного "
                "подписания соглашения об обработке "
                "персональных данных."
            ),
        }

    except MISUnavailableError:
        medical_data = {
            "available": False,
            "items": [],
            "page": 1,
            "pages": 1,
            "page_size": 10,
            "total": 0,
            "message": (
                "Система МИС временно недоступна. "
                "Попробуйте позже."
            ),
        }

    except MISNotFoundError:
        medical_data = {
            "available": False,
            "items": [],
            "page": 1,
            "pages": 1,
            "page_size": 10,
            "total": 0,
            "message": (
                "Медицинские данные пациента не найдены."
            ),
        }

    return render(
        request,
        "cabinet/patient_cabinet.html",
        {
            "nearest_appointment": nearest_appointment,
            "upcoming_appointments": upcoming_appointments,
            "appointments_available": appointments_available,
            "appointments_message": appointments_message,
            "medical_data": medical_data,
        }
    )
    
@login_required(login_url="cabinet:login")
def cancel_appointment_view(request, appointment_id):

    if request.method != "POST":
        return redirect("cabinet:patient_cabinet")

    patient_id = request.user.mis_patient_id

    try:
        AppointmentService.cancel_appointment(
            patient_id=patient_id,
            appointment_id=appointment_id,
        )

        messages.success(
            request,
            "Запись успешно отменена.",
        )

    except MISConflictError as exc:
        messages.error(
            request,
            str(exc),
        )

    except MISUnavailableError:
        messages.error(
            request,
            "Система МИС временно недоступна. Попробуйте позже.",
        )

    except MISNotFoundError:
        messages.error(
            request,
            "Запись не найдена.",
        )

    return redirect("cabinet:patient_cabinet")    
    
@login_required(login_url="cabinet:login")
def appointment_view(request):
    # Явное начало новой записи.
    if request.GET.get("new") == "1":
        AppointmentService.clear_booking_session(request)

        request.session["appointment_step"] = "step_1"

        return redirect("cabinet:appointment")

    current_step = request.session.get(
        "appointment_step",
        "step_1",
    )

    active_category = request.GET.get(
        "category",
        "consultation",
    )

    parent_id = request.GET.get("parent")

    if request.method == "POST":
        if current_step == "step_1":
            service_id = request.POST.get("service_id")

            if not service_id:
                messages.error(request, "Пожалуйста, выберите конкретную услугу из списка.")
                return redirect("cabinet:appointment")

            request.session["selected_service_id"] = service_id
            request.session["appointment_step"] = "step_2"
            return redirect("cabinet:appointment")

        if current_step == "step_2":

            # Возврат к выбору услуги
            if "back_to_services" in request.POST:
                request.session["appointment_step"] = "step_1"
                request.session.pop("selected_slot_id", None)

                return redirect("cabinet:appointment")

            service_id = request.session.get("selected_service_id")
            slot_id = request.POST.get("slot_id")
            selected_date = request.GET.get("date")

            try:
                selected_slot = AppointmentService.select_slot(
                    service_id=service_id,
                    slot_id=slot_id,
                    selected_date=selected_date,
                )

            except ValueError as exc:
                messages.error(
                    request,
                    str(exc),
                )

                return redirect("cabinet:appointment")

            # Сохраняем только ID выбранного слота.
            # Дату и время больше не дублируем в session.
            request.session["selected_slot_id"] = selected_slot["id"]

            # Переходим к подтверждению записи.
            request.session["appointment_step"] = "step_3"

            return redirect("cabinet:appointment")
                    
        if current_step == "step_3":

            # Вернуться к выбору даты и времени
            if "back_to_slots" in request.POST:
                request.session["appointment_step"] = "step_2"
                return redirect("cabinet:appointment")

            patient_id = request.user.mis_patient_id
            slot_id = request.session.get("selected_slot_id")

            try:
                appointment = AppointmentService.confirm_appointment(
                    patient_id=patient_id,
                    slot_id=slot_id,
                )

            except ValueError as exc:
                messages.error(
                    request,
                    str(exc),
                )
                return redirect("cabinet:appointment")

            except MISConflictError as exc:
                messages.error(
                    request,
                    str(exc),
                )
                return redirect("cabinet:appointment")

            except MISUnavailableError:
                messages.error(
                    request,
                    "Система МИС временно недоступна. Попробуйте позже.",
                )
                return redirect("cabinet:appointment")

            request.session["appointment_success"] = {
            "id": appointment["id"],
            "service": appointment["service"],
            "doctor": appointment["doctor"],
            "price": appointment["price"],
            "date": appointment["date"].isoformat(),
            "time": appointment["time"].isoformat(),
            "status": appointment["status"],
        }

        AppointmentService.clear_booking_session(request)

        return redirect("cabinet:appointment_success")

    # Данные для шаблона
    services = []
    slots = []
    available_dates = []
    selected_date = request.GET.get("date")
    selected_service = None
    selected_slot = None


    # =========================================================
    # ШАГ 1 — выбор услуги
    # =========================================================

    if current_step == "step_1":

        try:
            services = AppointmentService.get_services(
                category=active_category,
                parent_id=parent_id,
            )

        except MISUnavailableError:
            messages.error(
                request,
                "Система МИС временно недоступна. Попробуйте позже.",
            )
            services = []

        except MISNotFoundError:
            messages.error(
                request,
                "Запрашиваемые услуги не найдены.",
            )
            services = []


    # =========================================================
    # ШАГ 2 — выбор даты и времени
    # =========================================================

    elif current_step == "step_2":

        service_id = request.session.get(
            "selected_service_id"
        )

        if not service_id:
            messages.error(
                request,
                "Не удалось определить выбранную услугу.",
            )
            return redirect("cabinet:appointment")

        try:
            selected_service = AppointmentService.get_service(
                service_id
            )

            all_slots = AppointmentService.get_available_slots(
                service_id
            )

        except MISUnavailableError:
            messages.error(
                request,
                "Система МИС временно недоступна. Попробуйте позже.",
            )
            selected_service = None
            all_slots = []
            available_dates = []
            slots = []

        except MISNotFoundError:
            messages.error(
                request,
                "Выбранная услуга больше недоступна.",
            )
            selected_service = None
            all_slots = []
            available_dates = []
            slots = []

        available_dates = sorted({
            slot["date"]
            for slot in all_slots
        })

        if selected_date:
            slots = [
                slot
                for slot in all_slots
                if slot["date"].isoformat() == selected_date
            ]


    # =========================================================
    # ШАГ 3 — подтверждение
    # =========================================================

    elif current_step == "step_3":

        service_id = request.session.get(
            "selected_service_id"
        )

        slot_id = request.session.get(
            "selected_slot_id"
        )

        if not service_id or not slot_id:
            messages.error(
                request,
                "Не удалось определить данные выбранной записи.",
            )
            return redirect("cabinet:appointment")

        try:
            selected_service = AppointmentService.get_service(
                service_id
            )

            selected_slot = AppointmentService.get_slot(
                service_id,
                slot_id,
            )

        except MISUnavailableError:
            messages.error(
                request,
                "Система МИС временно недоступна. Попробуйте позже.",
            )
            selected_service = None
            selected_slot = None

        except MISNotFoundError:
            messages.error(
                request,
                "Выбранная услуга или время больше недоступны.",
            )
            selected_service = None
            selected_slot = None

        else:
            if selected_slot is None:
                messages.error(
                    request,
                    "Выбранный слот больше недоступен.",
                )
                return redirect("cabinet:appointment")


    return render(
        request,
        "cabinet/appointment.html",
        {
            "current_step": current_step,
            "active_category": active_category,
            "parent_id": parent_id,
            "services": services,
            "slots": slots,
            "available_dates": available_dates,
            "selected_date": selected_date,
            "selected_service": selected_service,
            "selected_slot": selected_slot,
        },
    )
    
    
    
@login_required(login_url="cabinet:login")
def appointment_success_view(request):
    appointment = request.session.pop(
        "appointment_success",
        None,
    )

    if not appointment:
        return redirect("cabinet:appointment")

    appointment["date"] = date.fromisoformat(
        appointment["date"]
    )

    appointment["time"] = time.fromisoformat(
        appointment["time"]
    )

    return render(
        request,
        "cabinet/appointment_success.html",
        {
            "appointment": appointment,
        },
    )
    
    
    
@login_required(login_url="cabinet:login")
def medical_record_detail_view(
    request,
    record_id,
):
    patient_id = request.user.mis_patient_id

    try:
        record = MedicalRecordService.get_patient_record(
            patient_id,
            record_id,
        )

    except MISPermissionError:
        return JsonResponse(
            {
                "error": "Доступ к медицинским данным запрещён."
            },
            status=403,
        )

    except MISNotFoundError:
        return JsonResponse(
            {
                "error": "Медицинская запись не найдена."
            },
            status=404,
        )

    return JsonResponse(record)