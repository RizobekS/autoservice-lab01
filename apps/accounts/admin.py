from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from .models import User, Appointment, ShortAppointment


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'phone', 'branch', 'status', 'datetime')
    list_editable = ('status',)
    list_filter = ('branch', 'status', 'datetime')


@admin.register(ShortAppointment)
class ShortAppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'branch', 'datetime')
    list_filter = ('branch', 'datetime')
