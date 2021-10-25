from django.contrib.sitemaps import Sitemap, GenericSitemap
from django.urls import reverse

from apps.cars.sitemap import CarsSitemap
from apps.editor_pages.models import EditorPage
from apps.knowledge_base.models import FaqEntry, Symptom
from apps.news.models import Article
from apps.promotions.models import Promotion
from apps.services.models import Section, Product
from apps.services.sitemap import product_sitemaps

from apps.work_gallery.models import Work


class StaticSitemaps(Sitemap):
    """ All static views are defined here """

    def items(self):
        return [
            'about:about',
            'contacts:contacts',
            'home:index',
            'knowledge_base:list',
            'promotions:list'
            'services:spare_parts',
            'work_gallery:list',
            'static:certificates',
        ]

    def location(self, item):
        return reverse(item)


def sitemap_factory(queryset):
    """ Just a handy shortcut """
    return GenericSitemap({'queryset': queryset})


print('ex')
sitemaps = {
    'cars': CarsSitemap,

    'editor_pages': sitemap_factory(EditorPage.objects.filter(active=True)),

    # Knowledge base
    'faq_entries': sitemap_factory(FaqEntry.objects.filter(answered=True)),
    'symptoms': sitemap_factory(Symptom.objects.filter(active=True)),

    'news': sitemap_factory(Article.objects.filter(status='published')),

    'promotions': sitemap_factory(Promotion.objects.filter(active=True)),

    # Services
    **product_sitemaps(),  # All products with all possible car filters
    'sections': sitemap_factory(Section.objects.filter(active=True)),
    'products': sitemap_factory(Product.objects.filter(active=True)),  # Bare products

    'work_gallery': sitemap_factory(Work.objects.filter(active=True)),

    # All static views
    'static_view_pages': StaticSitemaps,
}
