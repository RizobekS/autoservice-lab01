from typing import Dict, Any, List

from django.views.generic.base import ContextMixin

from apps.services.models import Product, Section


class ProductsMixin(ContextMixin):
    """
        Adds product list to your context

        products_context_name: str - name which list will have in context (default is "products")
        products_max: int - max number of product objects passed to context (default is None, which is infinity)
        products_additional_kwargs: dict - additional keyword arguments for db query
    """
    products_context_name: str = 'products'
    products_max: int = None
    products_additional_kwargs: dict = {}

    def get_products(self) -> List[Product]:
        products = Product.objects.filter(active=True, **self.products_additional_kwargs)
        return products[:self.products_max] if self.products_max else products

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context[self.products_context_name] = self.get_products()
        return context


class SectionsMixin(ContextMixin):
    """
        Adds section list to your context

        sections_context_name: str - name which list will have in context (default is "sections")
        sections_max: int - max number of section objects passed to context (default is None, which is infinity)
        sections_additional_kwargs: dict - additional keyword arguments for db query
    """
    sections_context_name: str = 'sections'
    sections_max: int = None
    sections_additional_kwargs: dict = {}

    def get_sections(self) -> List[Section]:
        sections = Section.objects.filter(active=True, **self.sections_additional_kwargs)
        return sections[:self.sections_max] if self.sections_max else sections

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context[self.sections_context_name] = self.get_sections()
        return context
