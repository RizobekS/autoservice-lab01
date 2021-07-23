from django.contrib import admin
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from apps.cars.models import Vendor, Model, Year, Modification
from utils.admin_actions import activate, deactivate, clone


@admin.register(Vendor)
class VendorAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'url', 'active', 'related_cars')
    list_filter = ('active',)
    search_fields = ('name', 'model__name', 'model__year__year', 'model__year__modification__name')
    prepopulated_fields = {'url': ('name',), }
    actions = (activate, deactivate, clone)

    @admin.display(description='Связанные модели')
    def related_cars(self, obj):
        cars = obj.model_set
        if obj.model_set.count() > 4:
            return f'Модели ({obj.model_set.count()})'
        else:
            return ', '.join([car.name for car in cars.all()])


class ModificationNestedInline(NestedStackedInline):
    model = Modification
    extra = 1


class YearInline(NestedStackedInline):
    model = Year
    inlines = (ModificationNestedInline,)
    extra = 1


@admin.register(Model)
class ModelAdmin(NestedModelAdmin):
    list_display = ('__str__', 'url', 'detailed_info')
    list_filter = ('vendor',)
    search_fields = ('name', 'vendor__name', 'year__year', 'year__modification__name')
    prepopulated_fields = {'url': ('name',), }
    inlines = (YearInline,)

    @admin.display(description='Года выпуска')
    def detailed_info(self, obj):
        years = obj.year_set
        if years.count() > 6:
            return f'{years.count()} разных годов выпуска'
        else:
            return mark_safe(', '.join([f'{year.year} <span style="color: grey">({year.modification_set.count()})</span>' for year in years.all()]))

    class Media:
        css = {
            'all': (static('/css/custom-admin/nested-inlines.css'),)
        }
