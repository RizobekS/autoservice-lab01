from django.contrib import admin
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin

from utils.admin_actions import clone, activate, deactivate
from utils.helpers import admin_reverse
from .forms import PromotionAdminForm
from .models import Category, Promotion


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'url', 'promotions_string')
    readonly_fields = ('promotions_string',)
    prepopulated_fields = {'url': ('name',), }

    list_display = ('name', 'url', 'promotions_string')
    list_filter = ('promotion',)
    search_fields = ('name', 'url')

    @admin.display(description='Привязанные Акции')
    def promotions_string(self, obj):
        return mark_safe(f'({obj.promotion_set.count()}) {" ,  ".join(admin_reverse(item, item.title) for item in obj.promotion_set.all())}')


@admin.register(Promotion)
class PromotionAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'active', 'category', 'tag_string', 'verbose_price', 'date', 'show_at_homepage')
    list_editable = ('show_at_homepage',)
    list_filter = ('active', 'category', 'tags', 'date', 'fixed_price')
    search_fields = ('title', 'short_description', 'homepage_description', 'text')
    actions = (activate, deactivate, clone)

    prepopulated_fields = {'url': ('title',), }
    autocomplete_fields = ('category', 'tags')
    radio_fields = {'sale': admin.HORIZONTAL}
    fieldsets = (
        (None, {'fields': (('title', 'url'), 'active', 'category', 'tags', 'date', 'sale', ('price', 'fixed_price'))}),
        ('Изображение', {'fields': ('image', 'thumbnail', 'icon_thumbnail'), 'classes': ['wide']}),
        ('Главная страница', {'fields': ('show_at_homepage', 'homepage_description'), 'classes': ['wide', 'collapse']}),
        ('Текст', {'fields': ('short_description', 'text'), 'classes': ['wide']}),
    )
    form = PromotionAdminForm
