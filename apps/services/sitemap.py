from typing import Dict

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.services.models import Product
from apps.services.utils.cached_cars import create_cached_car_url_list


class ProductSitemap(Sitemap):
    __slots__ = ['product_url']

    def location(self, item):
        return reverse('services:product_car', args=(self.product_url, item))


def _sitemap_factory(product, cached_car_pack) -> type:
    new_sitemap_class = type('ProductCarSitemap', (ProductSitemap,), {'product_url': product.url, 'items': cached_car_pack})
    return new_sitemap_class


def product_sitemaps() -> Dict[str, type]:
    """
        Returns dictionary {<product-slug>: <sitemap-class-for-this-product>}
        Caches computed url components into cached_car_packs dict, which has separate key for each car pack and None for car_pack with all cars included
    """
    cached_car_packs = {}  # All cached car_packs are stored here (car_packs including all cars also)

    sitemaps = {}
    for product in Product.objects.filter(active=True):

        if product.car_pack not in cached_car_packs:  # Create cached car pack for the product's car pack if does not exist
            cached_car_packs[product.car_pack] = create_cached_car_url_list(product.car_pack)

        sitemaps[product.url] = _sitemap_factory(product, cached_car_packs[product.car_pack])

    return sitemaps
