from django.contrib import admin
from image_cropping import ImageCroppingMixin

from utils.admin_actions import clone, activate, deactivate
from .forms import EditorPageForm
from .models import EditorPage


@admin.register(EditorPage)
class EditorPageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'active',)
    list_editable = ('active',)
    list_filter = ('active',)
    search_fields = ('url', 'content')
    actions = (activate, deactivate, clone)
    readonly_fields = ('url',)

    fieldsets = (
        (None, {'fields': (('title', 'url'), 'content')}),
        ('CEO настройки', {'fields': ('meta_description', 'meta_keywords', 'meta_robots'), 'classes': ['wide']})
    )
    form = EditorPageForm

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
