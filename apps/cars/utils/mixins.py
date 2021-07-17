from typing import Dict, Any, List

from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import ContextMixin

from apps.cars.models import Vendor
from utils.breadcrumbs.types import Breadcrumb
from utils.car_filter import remove_car_filter, set_car_filter
from utils.mixins import PageSettingsMixin


class VendorsMixin(ContextMixin):
    """
        Adds vendor list to your context

        vendors_context_name: str - name which list will have in context (default is "vendors")
        vendors_max: int - max number of vendor objects passed to context (default is None, which is infinity)
        vendors_additional_kwargs: dict - additional keyword arguments for db query
    """
    vendors_context_name: str = 'vendors'
    vendors_max: int = None
    vendors_additional_kwargs: dict = {}

    def get_vendors(self) -> List[Vendor]:
        vendors = Vendor.objects.filter(active=True, **self.vendors_additional_kwargs)
        return vendors[:self.vendors_max] if self.vendors_max else list(vendors)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        kwargs[self.vendors_context_name] = self.get_vendors()
        return super().get_context_data(**kwargs)


class CarFilterPageSettingsMixin(PageSettingsMixin):
    """
        Extends PageSettingsMixin functionality AND
        Determines whether there is a carfilter in urls
            If yes:
                adds extra breadcrumbs according to car_filter ,
                updates viewname (adds "_car"),
                adds context variable "selected_car",
                updates ceo context
            If no:
                adds context variable "selected_car",

        Requires self.viewname and self.kwargs

        car_filter_urls_name: str - name of urlpattern name, containing CarUrls object
        viewname_suffix: str - if set, appended to viewname attribute if car_filter in urls
    """
    car_filter_urls_name = 'urls'
    car_filter_context_name = 'car_filter'
    viewname_suffix = None

    def get_car_filter(self):
        if hasattr(self, 'car_filter'):
            return self.car_filter

        if hasattr(self, 'kwargs') and hasattr(self, 'request'):
            urls = self.kwargs.get()
            if urls:
                car_filter = urls.save(self.request)
                set_car_filter(self.request, car_filter)
            else:
                remove_car_filter(self.request)
                car_filter = None

            if self.viewname_suffix and car_filter:
                self.viewname = self.viewname + self.viewname_suffix
            self.car_filter = car_filter

            return car_filter
        else:
            raise ImproperlyConfigured('CarFilterPageSettingsMixin requires kwargs, request and viewname attributes set')

    def get_breadcrumbs(self):
        breadcrumbs = super().get_breadcrumbs()
        car_filter = self.get_car_filter()

        if car_filter:
            last_url = breadcrumbs[-1].url if len(breadcrumbs) else '/cars/'

            car_filter_url = "--".join(car_filter.vendor.url_args())
            breadcrumbs.append(Breadcrumb(car_filter.vendor.name, f'{last_url}{car_filter_url}/'))
            if car_filter.model:
                car_filter_url = "--".join(car_filter.model.url_args())
                breadcrumbs.append(Breadcrumb(car_filter.model.name, f'{last_url}{car_filter_url}/'))
                if car_filter.year:
                    if car_filter.modification:
                        name = f'{car_filter.year.name} {car_filter.modification.name}'
                        url_args = car_filter.modification.url_args()
                    else:
                        name = car_filter.year.name
                        url_args = car_filter.year.url_args()
                    car_filter_url = "--".join(url_args)
                    breadcrumbs.append(Breadcrumb(name, f'{last_url}{car_filter_url}/'))
        return breadcrumbs

    def get_ceo_context(self):
        context = super().get_ceo_context()
        car_filter = self.get_car_filter()
        if car_filter:
            context.update({
                'vendor': car_filter.vendor.name if car_filter.vendor else '',
                'model': car_filter.model.name if car_filter.model else '',
                'year': car_filter.year.name if car_filter.year else '',
                'modification': car_filter.modification.name if car_filter.modification else '',
            })
        return context

    def get_context_data(self, **kwargs):
        car_filter = self.get_car_filter()
        kwargs.update({
            'selected_car': car_filter and car_filter.is_full(),
            self.car_filter_context_name: car_filter,
        })
        return super().get_context_data(**kwargs)
