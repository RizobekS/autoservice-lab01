from typing import Dict, Any, List

from django.db.models import QuerySet
from django.views.generic.base import ContextMixin

from apps.work_gallery.models import Category


class CategoriesMixin(ContextMixin):
    """
        Adds category list to your context

        categories_context_name: str - name which list will have in context (default is "categories")
        categories_max: int - max number of category objects passed to context (default is None, which is infinity)
        categories_queryset: QuerySet = queryset to use to retrieve data (default is Promotion.objects)
    """
    categories_context_name: str = 'categories'
    categories_max: int = None
    categories_queryset: QuerySet = Category.objects

    def get_categories_queryset(self):
        return self.categories_queryset

    def get_categories(self) -> List[Category]:
        categories = self.get_categories_queryset().filter(active=True)
        return categories[:self.categories_max] if self.categories_max else list(categories)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context[self.categories_context_name] = self.get_categories()
        return context
