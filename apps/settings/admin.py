from django.contrib import admin

from .models import StaticInformation, Branch, EmailReceiver


# admin.site.site_header = 'ATБ - Админ панель'

@admin.register(StaticInformation)
class StaticInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'add_to_context', 'value', 'key')
    list_editable = ('value',)

    readonly_fields = ('name', 'add_to_context', 'key')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class EmailReceiverInlineAdmin(admin.StackedInline):
    extra = 1
    model = EmailReceiver


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'address', 'phone', 'receivers_string')

    inlines = (EmailReceiverInlineAdmin,)
