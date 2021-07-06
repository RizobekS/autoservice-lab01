from django.contrib import admin

from apps.site_settings.models import EmailReceiver, Branch, StaticInformation

admin.site.site_header = 'EuroRepar - Админ панель'


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
