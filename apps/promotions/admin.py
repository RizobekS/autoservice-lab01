from django.contrib import admin
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin

from utils.admin_actions import clone, activate, deactivate
from utils.helpers import admin_reverse
from .forms import PromotionAdminForm
from .models import Category, Promotion
from ..site_settings.models import CEOSetting


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'url', 'promotions_string')}),
        ('CEO настройки (для привязанных акций)',
         {'fields': ('variables_safe', 'meta_title', 'meta_header', 'meta_description', 'meta_keywords', 'meta_robots'), 'classes': ['wide', 'collapse']})
    )
    readonly_fields = ('promotions_string', 'variables_safe')
    prepopulated_fields = {'url': ('name',), }

    list_display = ('name', 'url', 'promotions_string')
    list_filter = ('promotion',)
    search_fields = ('name', 'url')

    @admin.display(description='Привязанные Акции')
    def promotions_string(self, obj):
        return mark_safe(f'({obj.promotion_set.count()}) {" ,  ".join(admin_reverse(item, item.title) for item in obj.promotion_set.all())}')

    @admin.display(description='Доступные перменные')
    def variables_safe(self, *args):
        obj = CEOSetting.objects.get(key='promotions:promotion')
        return mark_safe(obj.variables.replace('{{', '<b>{{').replace('}}', '}}</b>'))

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('promotion_set')


@admin.register(Promotion)
class PromotionAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'absolute_url', 'active', 'active_before', 'category', 'tag_string', 'verbose_price', 'date', 'show_at_homepage')
    list_editable = ('show_at_homepage', 'absolute_url', 'active')
    list_filter = ('active', 'category', 'tags', 'date', 'fixed_price')
    search_fields = ('title', 'short_description', 'homepage_description', 'text')
    actions = (activate, deactivate, clone)

    prepopulated_fields = {'url': ('title',), }
    autocomplete_fields = ('category', 'tags')
    radio_fields = {'sale': admin.HORIZONTAL}
    filter_horizontal = ('articles', 'products')
    fieldsets = (
        (None, {'fields': (('title', 'url', 'absolute_url'), 'active', 'category', 'tags', 'specific_branch', 'date', 'active_before', 'sale', ('price', 'fixed_price'))}),
        ('Привязка к Статьям и Услугам', {'fields': ('articles', 'products'), 'classes': ['collapse']}),
        ('Изображение', {'fields': ('image', 'thumbnail', 'icon_thumbnail'), 'classes': ['wide']}),
        ('Главная страница', {'fields': ('show_at_homepage', 'homepage_description'), 'classes': ['wide', 'collapse']}),
        ('Текст', {'fields': ('short_description', 'text'), 'classes': ['wide']}),
        ('CEO настройки', {'fields': ('meta_title', 'meta_header', 'meta_description', 'meta_keywords', 'meta_robots'), 'classes': ['wide', 'collapse']})
    )
    form = PromotionAdminForm

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')
