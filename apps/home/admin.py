from adminsortable.admin import SortableAdmin
from django.contrib import admin

from apps.home.models import Slide
from image_cropping import ImageCroppingMixin


@admin.register(Slide)
class FaqEntryAdmin(ImageCroppingMixin, SortableAdmin):
    list_display = ( 'animated_text', 'static_text', 'active', 'link', 'button_text')
    list_filter = ('active',)
    list_editable = ('active',)
    search_fields = ('static_text', 'animated_text', 'button_text')

    fields = ('animated_text', 'static_text', 'description', ('button_text', 'link'), 'background_image')
