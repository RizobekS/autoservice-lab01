from django.contrib import admin
from image_cropping import ImageCroppingMixin

from utils.admin_actions import clone, activate, deactivate
from .forms import EditorPageForm
from .models import EditorPage


@admin.register(EditorPage)
class EditorPageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'active', 'show_in_menu', 'show_in_footer')
    list_editable = ('active', 'show_in_menu', 'show_in_footer')
    list_filter = ('active', 'show_in_menu', 'show_in_footer')
    search_fields = ('url', 'content')
    actions = (activate, deactivate, clone)
    # readonly_fields = ('url',)

    fieldsets = (
        (None, {'fields': (('title', 'url'), ('active', 'show_in_menu', 'show_in_footer'), 'content')}),
        ('CEO настройки', {'fields': ('meta_description', 'meta_keywords', 'meta_robots'), 'classes': ['wide']})
    )
    form = EditorPageForm
