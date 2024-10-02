from adminsortable.admin import SortableAdmin
from django.contrib import admin

from apps.home.models import Slide


@admin.register(Slide)
class FaqEntryAdmin(SortableAdmin):
    list_display = ('static_text', 'animated_text', 'active', 'link', 'button_text')
    list_filter = ('active',)
    list_editable = ('active',)
    search_fields = ('static_text', 'animated_text', 'button_text')

    fields = ('static_text', 'animated_text', ('button_text', 'link'), 'background_image')
