from typing import Dict, Union

from django.contrib.sitemaps import Sitemap
from django.db import OperationalError
from django.urls import reverse

from apps.services.models import Product, Section
from apps.services.utils.cached_cars import create_cached_car_url_list


class ProductSitemap(Sitemap):
    __slots__ = ['product_url']

    def location(self, item):
        return reverse('services:product_car', args=(self.product_url, item))


class SectionSitemap(Sitemap):
    __slots__ = ['section_url']

    def location(self, item):
        return reverse('services:section_car', args=(self.section_url, item))


def _sitemap_factory(service: Union[Section, Product], cached_car_pack) -> type:
    new_sitemap_class = type('ProductCarSitemap', (ProductSitemap,), {'product_url': service.url, 'items': cached_car_pack})
    return new_sitemap_class


def service_sitemaps() -> Dict[str, type]:
    """
        Returns dictionary {<product-slug>: <sitemap-class-for-this-product>}
        Caches computed url components into cached_car_packs dict, which has separate key for each car pack and None for car_pack with all cars included
    """
    sitemaps = {}

    try:
        cached_car_packs = {}  # All cached car_packs are stored here (item which includes all cars is also)

        for section in Section.objects.filter(active=True, canonical_to_original=False):
            if None not in cached_car_packs:  # Sections support all cars, so car_pack is always None
                cached_car_packs[None] = create_cached_car_url_list(None)

            sitemaps[section.url] = _sitemap_factory(section, cached_car_packs[None])

        for product in Product.objects.filter(active=True, canonical_to_original=False):

            if product.car_pack not in cached_car_packs:  # Create cached car pack for the product's car pack if does not exist
                cached_car_packs[product.car_pack] = create_cached_car_url_list(product.car_pack)

            sitemaps[product.url] = _sitemap_factory(product, cached_car_packs[product.car_pack])

    except OperationalError:
        print('Could not generate sitemap classes for Section and/or Product')
        print('Ignore this message if you running "makemigrations" or "migrate"')
    return sitemaps
