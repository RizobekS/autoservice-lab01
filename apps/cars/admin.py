from django.contrib import admin
from django.db.models import Count
from django.http import HttpResponse
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from apps.cars.excel import export_cars
from apps.cars.models import Vendor, Model, Year, Modification
from utils.admin_actions import activate, deactivate, clone


def export_cars_as_excel_view(request, *args, **kwargs):
    output = export_cars()
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=cars.xlsx'
    response.write(output)
    return response


@admin.register(Vendor)
class VendorAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'url', 'catalog', 'active', 'related_cars')
    list_filter = ('catalog', 'active')
    list_editable = ('catalog', 'active')
    fields = (('name', 'url'), 'catalog', 'logo', 'favicon', 'active', 'header_image', 'header_crop')
    search_fields = ('name', 'model__name', 'model__year__year', 'model__year__modification__name')
    prepopulated_fields = {'url': ('name',), }
    actions = (activate, deactivate, clone)

    def get_urls(self):
        """ Add export to excel to urls """
        from django.urls import path
        info = self.model._meta.app_label, self.model._meta.model_name
        return [path('export_excel/', export_cars_as_excel_view, name='%s_%s_export_excel' % info)] + super().get_urls()

    @admin.display(description='Связанные модели')
    def related_cars(self, obj):
        cars = obj.model_set
        if obj.model_count > 4:
            return f'Модели ({obj.model_count})'
        else:
            return ', '.join([car.name for car in cars.all()])

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('model_set').annotate(model_count=Count('model'))


class ModificationNestedInline(NestedStackedInline):
    fields = ('name', 'active')
    model = Modification
    extra = 1


class YearInline(NestedStackedInline):
    fields = ('year', 'active')
    model = Year
    inlines = (ModificationNestedInline,)
    extra = 1


@admin.register(Model)
class ModelAdmin(ImageCroppingMixin, NestedModelAdmin):
    list_display = ('__str__', 'url', 'detailed_info', 'active')
    list_filter = ('vendor', 'active')
    list_editable = ('active',)
    search_fields = ('name', 'vendor__name', 'year__year', 'year__modification__name')
    prepopulated_fields = {'url': ('name',), }
    inlines = (YearInline,)
    save_on_top = True

    @admin.display(description='Года выпуска')
    def detailed_info(self, obj):
        years = obj.year_set
        if obj.year_count > 6:
            return f'{obj.year_count} разных годов выпуска'
        else:
            return mark_safe(', '.join([f'{year.year} <span style="color: grey">({year.modification_set.count()})</span>' for year in years.all()]))

    def get_queryset(self, request):
        return super().get_queryset(request).filter(vendor__active=True).select_related('vendor').prefetch_related('year_set__modification_set').annotate(year_count=Count('year'))

    class Media:
        css = {
            'all': (static('/css/custom-admin/nested-inlines.css'),)
        }
