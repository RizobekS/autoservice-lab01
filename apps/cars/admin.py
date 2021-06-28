
from django.contrib import admin
from django.templatetags.static import static
from image_cropping import ImageCroppingMixin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from apps.cars.models import Vendor, Model, Year, Modification


@admin.register(Vendor)
class VendorAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'url', 'active', 'related_cars')
    prepopulated_fields = {'url': ('name',), }

class ModificationNestedInline(NestedStackedInline):
    model = Modification
    extra = 1

class YearInline(NestedStackedInline):
    model = Year
    inlines = (ModificationNestedInline, )
    extra = 1

@admin.register(Model)
class ModelAdmin(NestedModelAdmin):
    list_display = ('__str__', 'url', 'detailed_info')
    prepopulated_fields = {'url': ('name',), }
    inlines = (YearInline, )

    class Media:
        css = {
            'all': (static('/css/custom-admin/nested-inlines.css'), )
        }

