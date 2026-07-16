from adminsortable.admin import SortableAdmin
from django.contrib import admin
from django.db.models import Count, Sum, Prefetch
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
            'fields': ('icon', 'image', 'thumbnail_1960x600', 'thumbnail_960x585', 'thumbnail_455x200', 'thumbnail_348x236', 'thumbnail_268x118', 'thumbnail_80x80'),
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
        child_products = obj.active_child_product_set + obj.active_nephew_product_set
        count = obj.child_product_count + obj.nephew_product_count
        return mark_safe(f'<span style="margin-right: 60px">({count}) {", ".join(section.title for section in child_products)}</span>')

    @admin.display(description='Дочерние разделы')
    def child_sections(self, obj) -> str:
        section_set = obj.section_set.filter(active=True)
        return mark_safe(f'<span style="margin-right: 60px">({section_set.count()}) {", ".join(section.title for section in section_set.all())}</span>')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent_section__parent_section__parent_section').prefetch_related(
            Prefetch('child_product_set', queryset=Product.objects.filter(active=True), to_attr='active_child_product_set'),
            Prefetch('nephew_product_set', queryset=Product.objects.filter(active=True), to_attr='active_nephew_product_set')
        ).annotate(
            child_product_count=Count('child_product_set'), nephew_product_count=Count('nephew_product_set')
        )

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
        return obj.cars_count

    @admin.display(description='Привязанные услуги')
    def related_products(self, obj):
        return ', '.join(item.title for item in obj.product_set.all())

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(cars_count=Count('cars')).prefetch_related('product_set')


@admin.register(Product)
class ProductAdmin(ImageCroppingMixin, SortableAdmin):
    list_display = ('title', 'url', 'active', 'section', 'additional_sections_count', 'verbose_price', 'tag',
                    'canonical_to_original', 'show_in_promotions', 'show_at_homepage', 'template_without_design', 'description_length')
    list_editable = ('show_at_homepage', 'canonical_to_original', 'show_in_promotions', 'template_without_design')
    list_filter = ('active', 'fixed_price', 'show_at_homepage', 'section', 'tag', 'car_pack')
    search_fields = ('title', 'url', 'price', 'time_duration', 'car_pack__name', 'short_description', 'description')

    filter_horizontal = ('spare_parts', 'similar_products', 'additional_sections')
    prepopulated_fields = {'url': ('title',), }
    actions = (activate, deactivate, clone)

    save_on_top = True

    fieldsets = (
        (None, {
            'fields': (('title', 'url'), 'active', 'show_at_homepage', 'template_without_design', 'warranty', 'tag', 'section', 'additional_sections', ('price', 'fixed_price'),
                       'time_duration', 'spare_parts', 'car_pack', 'branches', 'similar_products')
        }),
        ('Текст', {'fields': ('short_description', 'anons', 'description', 'master_advise'), 'classes': ('wide',)}),
        ('Главная страница (Список акций)', {'fields': ('show_in_promotions', 'homepage_description'), 'classes': ['wide', 'collapse']}),
        ('Изображения', {
            'fields': ('icon', 'image', 'thumbnail_1960x600', 'thumbnail_960x585', 'thumbnail_455x200', 'thumbnail_348x236', 'thumbnail_268x118', 'thumbnail_80x80')
        }),
        ('CEO настройки', {'fields': ('canonical_to_original', 'meta_title', 'meta_header', 'meta_description', 'meta_keywords', 'meta_robots'), 'classes': ['wide', 'collapse']})
    )

    form = ProductAdminForm

    @admin.display(description='Длина текста')
    def description_length(self, obj):
        return len(obj.description)

    @admin.display(description='Доп. родители')
    def additional_sections_count(self, obj):
        return f'({obj.additional_sections_count})' if obj.additional_sections_count != 0 else '-'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(additional_sections_count=Count('additional_sections'))


@admin.register(SparePart)
class SparePartAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'url', 'verbose_price', 'active')
    list_filter = ('fixed_price',)
    list_editable = ('active',)
    search_fields = ('title', 'url', 'price')
    actions = (clone,)

    fields = ('title', 'url', 'bound_products', 'active', 'image', 'thumbnail_268x118', ('price', 'fixed_price'))
    prepopulated_fields = {'url': ('title',), }
    readonly_fields = ('bound_products',)

    @admin.display(description='Привязанные Товары/Услуги')
    def bound_products(self, obj: SparePart):
        return ' ,  '.join(item.title for item in obj.product_set.all())
