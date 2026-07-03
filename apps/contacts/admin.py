from django.contrib import admin

from apps.contacts.models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'text')
    readonly_fields = ('created_at',)
