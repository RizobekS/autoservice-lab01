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

    remainder = 0

    def get(self, request, tag=None):
        ARTICLES_PER_PAGE = 2
        PROMOTIONS_PER_PAGE = 2
        PRODUCTS_PER_PAGE = 2
        MASTERS_PER_PAGE = 4

        articles = self._get_slice(Article.objects.filter(status='published', **{'tags__url': tag} if tag else {}), ARTICLES_PER_PAGE)
        promotions = self._get_slice(Promotion.objects.filter(active=True, **{'tags__url': tag} if tag else {}), PROMOTIONS_PER_PAGE)
        products = self._get_slice(Product.objects.filter(active=True, **{'tag__url': tag} if tag else {}), PRODUCTS_PER_PAGE)
        masters_count = Master.objects.filter(active=True).count()
        masters = list(Master.objects.filter(active=True, id__in=[randint(1, masters_count) for item in range(0, 20)])[:MASTERS_PER_PAGE])

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
        per_page += self.remainder  # Append previous number of missing pages
        self._update_maximum(query_set.count() / per_page)
        _slice = list(query_set[page * per_page: (page + 1) * per_page])
        self.remainder = max(per_page - len(_slice), 0)  # Count number of missing items
        return _slice

    def _get_page(self):
        return int(self.request.GET.get('page', 1))

    def _update_maximum(self, new):
        self.max_pages = max(ceil(new), self.max_pages)
