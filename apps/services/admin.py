from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .forms import SectionAdminForm, ProductAdminForm
from .models import *


@admin.register(Section)
class SectionAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'active', 'parent_section', 'verbose_level', 'child_products')
    list_filter = ('active', 'parent_section')
    search_fields = ('title', 'url', 'title_dative', 'short_description', 'description')

    readonly_fields = ('child_products', 'child_sections')
    prepopulated_fields = {'url': ('title',), }

    save_on_top = True

    fieldsets = (
        (None, {
            'fields': (('title', 'url'), 'title_dative', 'active', 'parent_section', ('child_sections', 'child_products'))
        }),
        ('Текст', {
            'fields': ('short_description', 'description'),
            'classes': ('wide',)
        }),
        ('Изображения', {
            'fields': ('image', 'thumbnail_1960x600', 'thumbnail_960x585', 'thumbnail_455x200', 'thumbnail_348x236', 'thumbnail_268x118', 'thumbnail_80x80')
        }),
    )

    form = SectionAdminForm


@admin.register(Product)
class ProductAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'active', 'section', 'verbose_price', 'time_duration', 'show_at_homepage', 'tag')
    list_editable = ('show_at_homepage',)
    list_filter = ('active', 'fixed_price', 'show_at_homepage', 'section', 'tag')
    search_fields = ('title', 'url', 'section', 'price', 'time_duration', 'cars', 'short_description', 'description')

    filter_horizontal = ('spare_parts', 'cars')
    prepopulated_fields = {'url': ('title',), }

    save_on_top = True

    fieldsets = (
        (None, {
            'fields': (('title', 'url'), 'active', 'show_at_homepage', 'tag', 'section', ('price', 'fixed_price'), 'time_duration', 'spare_parts', 'cars')
        }),
        ('Текст', {
            'fields': ('short_description', 'description'),
            'classes': ('wide',)
        }),
        ('Изображения', {
            'fields': ('image', 'thumbnail_1960x600', 'thumbnail_960x585', 'thumbnail_455x200', 'thumbnail_348x236', 'thumbnail_268x118', 'thumbnail_80x80')
        }),
    )

    form = ProductAdminForm


@admin.register(SparePart)
class SparePartAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'verbose_price')
    list_filter = ('fixed_price',)
    search_fields = ('title', 'url', 'price')

    fields = ('title', 'url', 'image', 'product_thumbnail', ('price', 'fixed_price'))
    prepopulated_fields = {'url': ('title',), }
