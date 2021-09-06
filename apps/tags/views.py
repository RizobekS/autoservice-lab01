from math import ceil
from random import shuffle, randint
from typing import Any, Dict

from django.db.models import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from apps.knowledge_base.models import FaqEntry, Symptom
from apps.masters.models import Master
from apps.news.models import Article
from apps.promotions.models import Promotion
from apps.services.models import Product
from apps.tags.models import Tag
from utils.breadcrumbs.types import Breadcrumb
from utils.breadcrumbs.utils import reverse_bc
from utils.mixins import PageSettingsMixin


class TagsListView(View, PageSettingsMixin):
    viewname = 'tags:all'

    max_pages = 1  # Maximum possible pages

    articles_per_page = 3
    promotions_per_page = 3
    faq_entries_per_page = 3
    symptoms_per_page = 3

    tag = None

    initial_breadcrumbs = [reverse_bc(viewname='tags:all')]

    def get(self, request, tag=None):
        self.tag = self._get_tag()

        self._count_overheads()

        articles = self._get_slice(Article.objects.exclude(tags=None).filter(status='published', **{'tags__url': tag} if tag else {}), self.articles_per_page)
        promotions = self._get_slice(Promotion.objects.exclude(tags=None).filter(active=True, **{'tags__url': tag} if tag else {}), self.promotions_per_page)
        faq_entries = self._get_slice(FaqEntry.objects.exclude(tags=None).filter(answered=True, **{'tags__url': tag} if tag else {}), self.faq_entries_per_page)
        symptoms = self._get_slice(Symptom.objects.exclude(tags=None).filter(active=True, **{'tags__url': tag} if tag else {}), self.symptoms_per_page)

        mix = articles + promotions + faq_entries + symptoms
        shuffle(mix)

        context = self.get_context_data()
        context.update({
            'items': mix,
            'current_page': self._get_page(),
            'page_numbers': range(1, self.max_pages + 1),
            'tag': self.tag,
        })

        return render(request, 'tags/tags.html', context)

    # #### OVERRIDDEN MIXIN METHODS ####

    def get_ceo_key(self):
        return 'tags:single' if self.tag else super().get_ceo_key()

    def get_current_breadcrumb(self):
        return [Breadcrumb(self.tag.name, reverse_lazy('tags:single', args=(self.tag.url,)))] if self.tag else []

    def get_ceo_context(self) -> Dict[str, Any]:
        context = super().get_ceo_context()
        context.update({'tag': self.tag})
        return context

    # #### PRIVATE METHODS ####

    def _get_tag(self):
        tag_url = self.kwargs.get('tag')
        return Tag.objects.get(url=tag_url) if tag_url else None

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
