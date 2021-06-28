from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .forms import SectionAdminForm, ProductAdminForm
from .models import *

# Register your models here.


@admin.register(Section)
class SectionAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'active', 'verbose_level', 'home_page')
    list_editable = ('home_page', )

    readonly_fields = ('child_products', )
    prepopulated_fields = {'url': ('title',), }

    fieldsets = (
        (None, {
            'fields': (('title', 'url'), 'title_dative', 'active', 'short_description', ('parent_section', 'child_products'), 'description')
        }),
        ('Изображения', {
            'fields': ('image', 'title_background', 'card_thumbnail', 'vendor_page_thumbnail'),
            'classes': ('wide',),
        }),
        ('Настройки появления на главной странице', {
            'fields': ('home_page', 'homepage_thumbnail'),
            'classes': ('collapse',),
        }),
    )

    form = SectionAdminForm


@admin.register(Product)
class ProductAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'active', 'section', 'time_duration', 'verbose_price', 'home_page', 'is_favourite')
    list_editable = ('home_page', 'is_favourite')

    filter_horizontal = ('spare_parts', 'cars')
    prepopulated_fields = {'url': ('title',), }

    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'active', 'section', 'time_duration', ('price', 'fixed_price'), 'spare_parts', 'cars', 'short_description', 'description')
        }),
        ('Обрезка изображений', {
            'fields': ('image', 'product_thumbnail', 'car_thumbnail', 'icon_thumbnail')
        }),
        ('Настройки появления на главной странице', {
            'classes': ('collapse', ),
            'fields': ('home_page', 'homepage_thumbnail')
        }),
        ('Настройки появления в избранных', {
            'classes': ('collapse',),
            'fields': ('is_favourite', 'favourite_text')
        }),
    )

    form = ProductAdminForm


@admin.register(SparePart)
class SparePartAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'verbose_price')
    fields = ('title', 'url', 'image', 'product_thumbnail', ('price', 'fixed_price'))
    prepopulated_fields = {'url': ('title',), }
