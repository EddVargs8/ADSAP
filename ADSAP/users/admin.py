from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email', 'numero_empleado')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    filter_horizontal = ['groups', 'user_permissions']

admin.site.register(CustomUser, CustomUserAdmin)
