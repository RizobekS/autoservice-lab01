from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin

from apps.work_gallery.forms import WorkAdminForm
from apps.work_gallery.models import Category, Image, Work, VendorModelPack
from utils.admin_actions import activate, deactivate, clone
from utils.helpers import admin_reverse, link_tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'url', 'active', 'works_string')
    readonly_fields = ('works_string',)
    prepopulated_fields = {'url': ('name',), }

    list_display = ('name', 'url', 'active', 'works_string')
    list_filter = ('work', 'active')
    search_fields = ('name', 'url')

    @admin.display(description='Привязанные Работы')
    def works_string(self, obj):
        return mark_safe(f'({obj.work_set.count()}) {" ,  ".join(admin_reverse(item, item.title) for item in obj.work_set.all())}')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('work_set')


class ImageInlineAdmin(ImageCroppingMixin, admin.StackedInline):
    fieldsets = (
        (None, {'fields': (('image', 'alt'), 'iframe_url')}),
        ('Обрезка изображений', {'fields': ('list_thumbnail', 'page_thumbnail'), 'classes': ('collapse',), 'description': 'Появится после первого сохранения'})
    )
    extra = 0
    model = Image

    class Media:
        css = {'all': (static('css/custom-admin/image-inlines.css'),)}


@admin.register(VendorModelPack)
class VendorModelPackAdmin(admin.ModelAdmin):
    list_display = ('name', 'models_count', 'related_works')
    fields = ('name', 'related_works', 'models')
    readonly_fields = ('related_works',)
    filter_horizontal = ('models',)

    @admin.display(description='Всего моделей')
    def models_count(self, obj):
        return obj.models.count()

    @admin.display(description='Привязанные работы')
    def related_works(self, obj):
        return ', '.join(item.title for item in obj.work_set.all())


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'active', 'category_string', 'main_image_url', 'cost_of_work', 'spare_part_of_work')
    list_filter = ('active', 'categories')
    search_fields = ('title', 'url', 'text')
    actions = (activate, deactivate, clone)

    fields = (('title', 'url'), 'main_image', 'active', 'categories', 'model_pack', 'products', 'cost_of_work', 'spare_part_of_work', 'text', 'multiple_images')
    prepopulated_fields = {'url': ('title',), }
    autocomplete_fields = ('categories',)
    filter_horizontal = ('products',)
    form = WorkAdminForm
    inlines = (ImageInlineAdmin,)

    @admin.display(description='Категории')
    def category_string(self, obj):
        return mark_safe(f'({obj.categories.count()}) {" ,  ".join(admin_reverse(item, item.name) for item in obj.categories.all())}')

    @admin.display(description='Основное изображение')
    def main_image_url(self, obj):
        overall = obj.image_set.count()
        if obj.main_image:
            return format_html('<a href="{}" class="image-preview">{}</a><span> ({} всего)</span>',
                               obj.main_image.image.url, 'Посмотреть', overall)
        return f'({overall} всего)'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_multiple_images(form.instance)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('categories', 'image_set')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'main_image':
            instance_id = request.resolver_match.kwargs.get('object_id')
            kwargs['queryset'] = Image.objects.filter(work_id=instance_id)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
