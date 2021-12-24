from adminsortable.admin import SortableAdmin
from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.site_settings.models import EmailReceiver, Branch, StaticInformation, CEOSetting, MenuServiceSorting
from utils.admin_actions import activate, deactivate, clone

admin.site.site_header = 'EuroRepar - Админ панель'


@admin.register(StaticInformation)
class StaticInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'add_to_context', 'value', 'key')
    list_filter = ('category',)
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
    list_filter = ('active',)
    actions = (activate, deactivate, clone)

    inlines = (EmailReceiverInlineAdmin,)

    @admin.display(description='Получатели эл. сообщений')
    def receivers_string(self, obj):
        emails = obj.get_email_list()
        return f'({len(emails)}) {" ,  ".join(emails)}'


@admin.register(CEOSetting)
class CEOSettingAdmin(admin.ModelAdmin):
    list_display = ('page', 'title', 'header', 'key', 'variables_safe')
    # list_editable = ('title',)
    ordering = ('key', 'title')
    search_fields = ('page', 'title', 'header', 'key', 'description', 'keywords', 'robots')
    readonly_fields = ('variables_safe', 'page', 'key')
    fields = ('title', 'header', ('page', 'key'), 'description', 'keywords', 'robots')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description='Доступные переменные')
    def variables_safe(self, obj):
        return mark_safe(obj.variables.replace('{{', '<b>{{').replace('}}', '}}</b>')) if obj.variables else '-'


@admin.register(MenuServiceSorting)
class MenuServiceSortingAdmin(SortableAdmin):
    list_display = ('__str__', 'active')
    list_editable = ('active',)
    actions = (activate, deactivate)

    def get_list_display_links(self, request, list_display):
        return []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow cascade deletion (i.e. allow deletion of product/section, which will cascade to deletion of MenuServiceSorting instance)
        if '/product' in request.path_info and '/delete' in request.path_info:
            return super().has_delete_permission(request, obj)
        else:  # Do not allow direct deletion of menu entries
            return False
