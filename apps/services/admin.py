from adminsortable.admin import SortableAdmin
from django.contrib import admin
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin

from utils.admin_actions import clone, deactivate, activate
from .forms import SectionAdminForm, ProductAdminForm
from .models import Section, Product, SparePart, CarPack


@admin.register(Section)
class SectionAdmin(ImageCroppingMixin, SortableAdmin):
    list_per_page = 400
    list_display = ('title', 'url', 'active', 'parent_section', 'child_products', 'show_at_homepage')
    list_editable = ('show_at_homepage',)
    list_filter = ('active', 'show_at_homepage', 'parent_section')
    search_fields = ('title', 'url', 'title_dative', 'short_description', 'description')

    readonly_fields = ('child_products', 'child_sections')
    prepopulated_fields = {'url': ('title',), }
    actions = (activate, deactivate, clone)

    save_on_top = True

    fieldsets = (
        (None, {
            'fields': (('title', 'url'), 'title_dative', 'active', 'parent_section', ('child_sections', 'child_products'))
        }),
        ('Текст', {'fields': ('short_description', 'description'), 'classes': ('wide',)}),
        ('Изображения', {
            'fields': ('image', 'thumbnail_1960x600', 'thumbnail_960x585', 'thumbnail_455x200', 'thumbnail_348x236', 'thumbnail_268x118', 'thumbnail_80x80'),
        }),
        ('CEO настройки', {'fields': ('canonical_to_original', 'meta_title', 'meta_header', 'meta_description', 'meta_keywords', 'meta_robots'), 'classes': ['wide', 'collapse']})
    )

    form = SectionAdminForm

    def get_fieldsets(self, request, obj=None):
        if obj is not None:
            self.fieldsets[2][1]['classes'] = ('collapse',)
        return self.fieldsets

    @admin.display(description='Дочерние товары/услуги')
    def child_products(self, obj) -> str:
        child_products = obj.product_set.filter(active=True)
        return mark_safe(f'<span style="margin-right: 60px">({child_products.count()}) {", ".join(section.title for section in child_products.all())}</span>')

    @admin.display(description='Дочерние разделы')
    def child_sections(self, obj) -> str:
        section_set = obj.section_set.filter(active=True)
        return mark_safe(f'<span style="margin-right: 60px">({section_set.count()}) {", ".join(section.title for section in section_set.all())}</span>')

    class Media:
        js = ('js/custom/admin/copy-event-listeners.js',)
        css = {
            'all': ('css/custom-admin/accordion.css',)
        }


@admin.register(CarPack)
class CarPackAdmin(admin.ModelAdmin):
    list_display = ('name', 'cars_count', 'related_products')
    fields = ('name', 'related_products', 'cars')
    readonly_fields = ('related_products',)
    filter_horizontal = ('cars',)

    @admin.display(description='Всего машин')
    def cars_count(self, obj):
        return obj.cars.count()

    @admin.display(description='Привязанные услуги')
    def related_products(self, obj):
        return ', '.join(item.title for item in obj.product_set.all())


@admin.register(Product)
class ProductAdmin(ImageCroppingMixin, SortableAdmin):
    list_display = ('title', 'url', 'active', 'section', 'additional_sections_count', 'verbose_price', 'tag',
                    'canonical_to_original', 'show_in_promotions', 'show_at_homepage', 'description_length')
    list_editable = ('show_at_homepage', 'canonical_to_original', 'show_in_promotions')
    list_filter = ('active', 'fixed_price', 'show_at_homepage', 'section', 'tag', 'car_pack')
    search_fields = ('title', 'url', 'price', 'time_duration', 'car_pack__name', 'short_description', 'description')

    filter_horizontal = ('spare_parts', 'similar_products', 'additional_sections')
    prepopulated_fields = {'url': ('title',), }
    actions = (activate, deactivate, clone)

    save_on_top = True

    fieldsets = (
        (None, {
            'fields': (('title', 'url'), 'active', 'show_at_homepage', 'tag', 'section', 'additional_sections', ('price', 'fixed_price'),
                       'time_duration', 'spare_parts', 'car_pack', 'branches', 'similar_products')
        }),
        ('Текст', {'fields': ('short_description', 'description'), 'classes': ('wide',)}),
        ('Главная страница (Список акций)', {'fields': ('show_in_promotions', 'homepage_description'), 'classes': ['wide', 'collapse']}),
        ('Изображения', {
            'fields': ('image', 'thumbnail_1960x600', 'thumbnail_960x585', 'thumbnail_455x200', 'thumbnail_348x236', 'thumbnail_268x118', 'thumbnail_80x80')
        }),
        ('CEO настройки', {'fields': ('canonical_to_original', 'meta_title', 'meta_header', 'meta_description', 'meta_keywords', 'meta_robots'), 'classes': ['wide', 'collapse']})
    )

    form = ProductAdminForm

    @admin.display(description='Длина текста')
    def description_length(self, obj):
        return len(obj.description)

    @admin.display(description='Доп. родители')
    def additional_sections_count(self, obj: Product):
        count = obj.additional_sections.count()
        return f'({count})' if count != 0 else '-'


@admin.register(SparePart)
class SparePartAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'verbose_price')
    list_filter = ('fixed_price',)
    search_fields = ('title', 'url', 'price')
    actions = (clone,)

    fields = ('title', 'url', 'image', 'thumbnail_268x118', ('price', 'fixed_price'))
    prepopulated_fields = {'url': ('title',), }
