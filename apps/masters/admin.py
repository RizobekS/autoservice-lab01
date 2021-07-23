from django.contrib import admin
from image_cropping import ImageCroppingMixin

from apps.masters.models import Master, Position
from utils.admin_actions import activate, deactivate, clone


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Master)
class MasterAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'active', 'position_string', 'credo', 'show_at_homepage')
    list_editable = ('show_at_homepage',)
    list_filter = ('active', 'show_at_homepage', 'positions')
    filter_horizontal = ('positions',)

    actions = (activate, deactivate, clone)
