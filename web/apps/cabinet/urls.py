from django.urls import path
from . import views

app_name = 'cabinet'    

urlpatterns = [
    path('register', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'), 
    path('login/', views.login_view, name='login'),
    path('cabinet/', views.patient_cabinet_view, name='patient_cabinet'),
    path('appointment/', views.appointment_view, name='appointment'),
    path("appointment/success/", views.appointment_success_view, name="appointment_success"),
    path(
    "appointments/<int:appointment_id>/cancel/",
    views.cancel_appointment_view,
    name="cancel_appointment",
),
    path(
    "medical-records/<int:record_id>/",
    views.medical_record_detail_view,
    name="medical_record_detail",
),
    # path("verify-phone/", views.verify_phone_view, name="verify_phone"),
    # path("set-password/", views.set_password_view, name="set_password"),
    # path('api/services/', views.proxy_get_services, name='proxy_services'),
    # path('api/services/<int:service_id>/children/', views.proxy_get_service_children, name='proxy_services_children'),

]
