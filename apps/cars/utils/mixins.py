from typing import Dict, Any, List

from django.views.generic.base import ContextMixin

from apps.cars.models import Vendor


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
        context = super().get_context_data(**kwargs)
        context[self.vendors_context_name] = self.get_vendors()
        return context
