from django.contrib import admin

from apps.about.forms import EditorContentForm
from apps.about.models import EditorContent


@admin.register(EditorContent)
class EditorContentAdmin(admin.ModelAdmin):
    fields = ('title', 'key', 'text')
    list_display = ('title', 'key')
    readonly_fields = ('title', 'key')
    form = EditorContentForm

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
