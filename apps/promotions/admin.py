from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from image_cropping import ImageCroppingMixin

from .forms import PromotionAdminForm
from .models import *


@admin.register(Promotion)
class PromotionAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'active', 'tag_string', 'verbose_price', 'date', 'show_at_homepage')
    list_editable = ('show_at_homepage',)
    list_filter = ('active', 'tags', 'date', 'fixed_price', 'price')
    search_fields = ('title', 'short_description', 'text')
    actions = ('activate', 'deactivate')

    prepopulated_fields = {'url': ('title',), }
    autocomplete_fields = ('tags',)
    fieldsets = (
        (None, {'fields': (('title', 'url'), 'active', 'show_at_homepage', 'tags', 'date', ('price', 'fixed_price'))}),
        ('Изображение', {'fields': ('image', 'thumbnail', 'icon_thumbnail'), 'classes': ['wide']}),
        ('Текст', {'fields': ('short_description', 'text'), 'classes': ['wide']}),
    )
    form = PromotionAdminForm

    @admin.display(description='Тэги')
    def tag_string(self, obj):
        return ', '.join(item.name for item in obj.tags.all())

    @admin.display(description='Деактивировать')
    def deactivate(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, ngettext('%d акция была успешно деактивирована.', '%d акции были успешно деактивированы.', updated) % updated, messages.SUCCESS)

    @admin.display(description='Активировать')
    def activate(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, ngettext('%d акция была успешно активирована.', '%d акции были успешно активированы.', updated) % updated, messages.SUCCESS)
