import re
from django import forms
from .models import User
import datetime


class UserLoginForm(forms.Form):
    # Имя поля совпадает с name="username" в HTML
    username = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={'id': 'phone', 'placeholder': '+7 (___) ___-__-__'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'password', 'placeholder': 'Введите пароль'})
    )
    remember_me = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(attrs={'id': 'remember_me'})
    )

class RegistrationForm(forms.Form):
    phone = forms.CharField(max_length=25, required=True)
    snils = forms.CharField(max_length=20, required=True)
    dob = forms.DateField(required=True)

    def clean_dob(self):
        """Жесткая проверка совершеннолетия (18+) на бэкенде"""
        dob = self.cleaned_data.get('dob')
        today = datetime.date.today()
        
        # Считаем возраст
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        if age < 18:
            raise forms.ValidationError("Регистрация на портале доступна только лицам старше 18 лет.")
            
        return dob

    def clean_phone(self):
        """Автоматическая очистка и валидация телефона"""
        raw_phone = self.cleaned_data.get('phone', '')
        clean_phone = re.sub(r'\D', '', raw_phone)
        
        if len(clean_phone) < 11:
            raise forms.ValidationError("Некорректный формат номера телефона.")
            
        if clean_phone.startswith('8'):
            clean_phone = '7' + clean_phone[1:]
            
        
        # Проверка по BPMN: занят ли телефон на портале
        if User.objects.filter(phone=clean_phone).exists():
            raise forms.ValidationError("Пользователь с таким номером телефона уже зарегистрирован.")
            
        return clean_phone

    def clean_snils(self):
        """Автоматическая очистка СНИЛС"""
        raw_snils = self.cleaned_data.get('snils', '')
        clean_snils = re.sub(r'\D', '', raw_snils)
        
        if len(clean_snils) != 11:
            raise forms.ValidationError("СНИЛС должен состоять из 11 цифр.")
            
        return clean_snils
