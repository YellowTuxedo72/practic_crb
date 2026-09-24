from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Просто показываем список полей, которые есть в базе
    list_display = ('phone', 'mis_patient_id', 'is_staff', 'date_joined', 'last_login')
    search_fields = ('phone', 'mis_patient_id')
    
    # Запрещаем создавать пользователей через кнопку "+" в админке
    def has_add_permission(self, request):
        return False
