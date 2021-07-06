from math import ceil
from random import shuffle

from django.db.models import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from apps.masters.models import Master
from apps.news.models import Article
from apps.promotions.models import Promotion
from apps.tags.models import Tag
from utils.breadcrumbs.mixins import PageTitleMixin
from utils.breadcrumbs.types import Breadcrumb


class TagsListView(View, PageTitleMixin):
    viewname = 'tags:all'
    page_title = 'Акции'

    max_pages = 1  # Maximum possible pages

    def get(self, request, tag=None):
        ARTICLES_PER_PAGE = 4
        PROMOTIONS_PER_PAGE = 4
        MASTERS_PER_PAGE = 4

        kwargs = self._get_filter_kwargs()

        articles = self._get_slice(Article.objects.filter(status='published', **kwargs), ARTICLES_PER_PAGE)
        promotions = self._get_slice(Promotion.objects.filter(active=True, **kwargs), PROMOTIONS_PER_PAGE)
        masters = self._get_slice(Master.objects.filter(active=True), MASTERS_PER_PAGE)

        mix = articles + promotions + [masters]
        shuffle(mix)

        if tag:
            tag = Tag.objects.get(url=tag)
            self.extra_breadcrumbs = Breadcrumb(tag.name, reverse_lazy('tags:single', args=(tag.url,)))

        context = self.get_context_data()
        context.update({
            'items': mix,
            'current_page': self._get_page(),
            'page_numbers': range(1, self.max_pages + 1),
            'tag': tag,
            'page_title': tag.name if tag else self.page_title
        })

        return render(request, 'tags/tags.html', context)

    def _get_slice(self, query_set: QuerySet, per_page: int):
        page = self._get_page() - 1
        self._update_maximum(query_set.count() / per_page)
        return list(query_set[page * per_page: (page + 1) * per_page])

    def _get_page(self):
        return self.request.GET.get('page', 1)

    def _get_filter_kwargs(self):
        tag = self.kwargs.get('tag')
        return {'tags__url': tag} if tag else {}

    def _update_maximum(self, new):
        self.max_pages = max(ceil(new), self.max_pages)
