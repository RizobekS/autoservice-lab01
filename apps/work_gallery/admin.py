from django.contrib import admin
from django.templatetags.static import static
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
    list_display = ('name', 'models_count')
    fields = ('name', 'related_products', 'models')
    readonly_fields = ('related_products',)
    filter_horizontal = ('models',)

    @admin.display(description='Всего моделей')
    def models_count(self, obj):
        return obj.models.count()

    # @admin.display(description='Привязанные услуги')
    # def related_products(self, obj):
    #     return ', '.join(item.title for item in obj.product_set.all())


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'active', 'category_string', 'images_string')
    list_filter = ('active', 'categories')
    search_fields = ('title', 'url', 'text')
    actions = (activate, deactivate, clone)

    fields = (('title', 'url'), 'active', 'categories', 'model_pack', 'products', 'text', 'multiple_images')
    prepopulated_fields = {'url': ('title',), }
    autocomplete_fields = ('categories',)
    filter_horizontal = ('products',)
    form = WorkAdminForm
    inlines = (ImageInlineAdmin,)

    @admin.display(description='Категории')
    def category_string(self, obj):
        return mark_safe(f'({obj.categories.count()}) {" ,  ".join(admin_reverse(item, item.name) for item in obj.categories.all())}')

    @admin.display(description='Изображения')
    def images_string(self, obj):
        return mark_safe(f'({obj.image_set.count()}) {" ,  ".join(link_tag(item.image.url, item.image.name.split("/")[-1]) for item in obj.image_set.all())}')

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_multiple_images(form.instance)
