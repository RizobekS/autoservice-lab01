from typing import Dict, Any, List

from django.db.models import QuerySet
from django.views.generic.base import ContextMixin

from apps.services.models import Product, Section


class SectionsMixin(ContextMixin):
    """
        Adds section list to your context

        sections_context_name: str - name which list will have in context (default is "sections")
        sections_max: int - max number of section objects passed to context (default is None, which is infinity)
        sections_queryset: QuerySet - queryset to use
    """
    sections_context_name: str = 'sections'
    sections_max: int = None
    sections_queryset: QuerySet = Section.objects

    def get_sections_queryset(self):
        return self.sections_queryset

    def get_sections(self) -> List[Section]:
        sections = self.get_sections_queryset().filter(active=True)
        return sections[:self.sections_max] if self.sections_max else sections

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        kwargs[self.sections_context_name] = self.get_sections()
        return super().get_context_data(**kwargs)


class ProductsMixin(ContextMixin):
    """
        Adds product list to your context

        products_context_name: str - name which list will have in context (default is "products")
        products_max: int - max number of product objects passed to context (default is None, which is infinity)
        products_queryset: QuerySet - queryset to use
    """
    products_context_name: str = 'products'
    products_max: int = None
    products_queryset: QuerySet = Product.objects

    def get_products_queryset(self):
        return self.products_queryset

    def get_products(self) -> List[Product]:
        products = self.get_products_queryset().filter(active=True)
        return products[:self.products_max] if self.products_max else products

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        kwargs[self.products_context_name] = self.get_products()
        return super().get_context_data(**kwargs)


class SingleSectionMixin(ContextMixin):
    section_context_name = 'current_section'
    section_url_kwarg = 'section_url'
    kwargs: {} = None

    def get_current_section(self):
        return Section.objects.get(active=True, url__exact=self.kwargs.get('section_url'))

    def get_context_data(self, **kwargs):
        kwargs[self.section_context_name] = self.get_current_section()
        return super().get_context_data(**kwargs)
#
#
# class SingleProductMixin(ContextMixin):
#     product_context_name = 'product'
#     product_url_kwarg = 'product_url'
#     product_queryset = Product
#     kwargs: {} = None
#
#     def get_current_product(self):
#         return product_queryset.get(active=True, url__exact=self.kwargs.get('section_url'))
#
#     def get_context_data(self, **kwargs):
#         kwargs[self.product_context_name] = self.get_current_section()
#         return super().get_context_data(**kwargs)
