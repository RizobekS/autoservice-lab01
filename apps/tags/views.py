from math import ceil
from random import shuffle, randint

from django.db.models import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from apps.masters.models import Master
from apps.news.models import Article
from apps.promotions.models import Promotion
from apps.services.models import Product
from apps.site_settings.utils.mixins import MetaTagsRenderer
from apps.tags.models import Tag
from utils.breadcrumbs.mixins import PageTitleMixin
from utils.breadcrumbs.types import Breadcrumb


class TagsListView(View, PageTitleMixin):
    viewname = 'tags:all'
    page_title = 'Теги'

    max_pages = 1  # Maximum possible pages

    articles_per_page = 4
    promotions_per_page = 4
    products_per_page = 4
    MASTERS_PER_PAGE = 4

    def get(self, request, tag=None):
        self._count_overheads()

        articles = self._get_slice(Article.objects.filter(status='published', **{'tags__url': tag} if tag else {}), self.articles_per_page)
        promotions = self._get_slice(Promotion.objects.filter(active=True, **{'tags__url': tag} if tag else {}), self.promotions_per_page)
        products = self._get_slice(Product.objects.filter(active=True, **{'tag__url': tag} if tag else {}), self.products_per_page)
        masters_count = Master.objects.filter(active=True).count()
        masters = list(Master.objects.filter(active=True, id__in=[randint(1, masters_count) for item in range(0, 20)])[:self.MASTERS_PER_PAGE])

        mix = articles + promotions + products + [masters]
        shuffle(mix)

        if tag:
            tag = Tag.objects.get(url=tag)
            self.extra_breadcrumbs = Breadcrumb(tag.name, reverse_lazy('tags:single', args=(tag.url,)))
            meta_tags = MetaTagsRenderer('tags:single', {'tag': tag.name})
        else:
            meta_tags = MetaTagsRenderer('tags:all')

        context = self.get_context_data()
        context.update({
            'items': mix,
            'current_page': self._get_page(),
            'page_numbers': range(1, self.max_pages + 1),
            'tag': tag,
            'page_title': tag.name if tag else self.page_title
        })
        context.update(meta_tags.as_context())

        return render(request, 'tags/tags.html', context)

    def _get_slice(self, query_set: QuerySet, per_page: int):
        page = self._get_page() - 1
        self._update_maximum(query_set.count() / per_page)
        return list(query_set[page * per_page: (page + 1) * per_page])

    def _get_page(self):
        return int(self.request.GET.get('page', 1))

    def _update_maximum(self, new):
        self.max_pages = max(ceil(new), self.max_pages)

    def _count_overheads(self):  # If one of models cannot return enough results, other models compensate the lackness
        page = self._get_page() + 1
        article = max(page * self.articles_per_page - Article.objects.filter(status='published').count(), 0)
        promotion = max(page * self.promotions_per_page - Promotion.objects.filter(active=True).count(), 0)
        product = max(page * self.products_per_page - Product.objects.filter(active=True).count(), 0)
        overhead = article + promotion + product
        available = []
        if article == 0:
            available.append(self.articles_per_page)
        if promotion == 0:
            available.append(self.promotions_per_page)
        if product == 0:
            available.append(self.products_per_page)
        for item in available:
            item += overhead // len(available)
