from typing import Dict, Any, List

from django.db.models import QuerySet, Q
from django.utils import timezone
from django.views.generic.base import ContextMixin

from apps.promotions.models import Promotion


class PromotionsMixin(ContextMixin):
    """
        Adds promotion list to your context

        promotions_context_name: str - name which list will have in context (default is "promotions")
        promotions_max: int - max number of promotion objects passed to context (default is None, which is infinity)
        promotions_queryset: QuerySet = queryset to use to retrieve data (default is Promotion.objects)
    """
    promotions_context_name: str = 'promotions'
    promotions_max: int = None
    promotions_queryset: QuerySet = Promotion.objects.select_related('category').prefetch_related('tags', 'articles', 'products')

    def get_promotions_queryset(self):
        today = timezone.now().date()
        return self.promotions_queryset.filter(
            Q(active_before__isnull=True) | Q(active_before__gte=today)
        )

    def get_promotions(self) -> List[Promotion]:
        promotions = self.get_promotions_queryset().filter(active=True)
        return promotions[:self.promotions_max] if self.promotions_max else list(promotions)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context[self.promotions_context_name] = self.get_promotions()
        return context
