from typing import Dict, Any, List

from django.views.generic.base import ContextMixin

from apps.masters.models import Master


class MastersMixin(ContextMixin):
    """
        Adds master list to your context

        masters_context_name: str - name which list will have in context (default is "masters")
        masters_max: int - max number of master objects passed to context (default is None, which is infinity)
        masters_additional_kwargs: dict - additional keyword arguments for db query
    """
    masters_context_name: str = 'masters'
    masters_max: int = None
    masters_additional_kwargs: dict = {}

    def get_masters(self) -> List[Master]:
        masters = Master.objects.filter(active=True, **self.masters_additional_kwargs)
        return masters[:self.masters_max] if self.masters_max else masters

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context[self.masters_context_name] = self.get_masters()
        return context
