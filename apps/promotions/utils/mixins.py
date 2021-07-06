from typing import Dict, Any, List

from django.views.generic.base import ContextMixin

from apps.promotions.models import Promotion


class PromotionsMixin(ContextMixin):
    """
        Adds promotion list to your context

        promotions_context_name: str - name which list will have in context (default is "promotions")
        promotions_max: int - max number of promotion objects passed to context (default is None, which is infinity)
        promotions_additional_kwargs: dict - additional keyword arguments for db query
        promotions_exclude_kwargs: dict - keywords to pass to exclude()
    """
    promotions_context_name: str = 'promotions'
    promotions_max: int = None
    promotions_additional_kwargs: dict = {}
    promotions_exclude_kwargs: dict = {}

    def get_promotions_exclude_kwargs(self) -> Dict[str, Any]:
        return self.promotions_exclude_kwargs

    def get_promotions(self) -> List[Promotion]:
        promotions = Promotion.objects.filter(active=True, **self.promotions_additional_kwargs).exclude(**self.get_promotions_exclude_kwargs())
        return promotions[:self.promotions_max] if self.promotions_max else list(promotions)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context[self.promotions_context_name] = self.get_promotions()
        return context
