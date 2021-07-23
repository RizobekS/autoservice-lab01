from django.contrib import admin
from image_cropping import ImageCroppingMixin

from utils.admin_actions import clone, activate, deactivate
from .forms import PromotionAdminForm
from .models import *


@admin.register(Promotion)
class PromotionAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'active', 'tag_string', 'verbose_price', 'date', 'show_at_homepage')
    list_editable = ('show_at_homepage',)
    list_filter = ('active', 'tags', 'date', 'fixed_price', 'price')
    search_fields = ('title', 'short_description', 'text')
    actions = (activate, deactivate, clone)

    prepopulated_fields = {'url': ('title',), }
    autocomplete_fields = ('tags',)
    fieldsets = (
        (None, {'fields': (('title', 'url'), 'active', 'show_at_homepage', 'tags', 'date', ('price', 'fixed_price'))}),
        ('Изображение', {'fields': ('image', 'thumbnail', 'icon_thumbnail'), 'classes': ['wide']}),
        ('Текст', {'fields': ('short_description', 'text'), 'classes': ['wide']}),
    )
    form = PromotionAdminForm
