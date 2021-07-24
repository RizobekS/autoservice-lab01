from typing import Any, Dict

from django.urls import reverse
from django.views.generic import DetailView, TemplateView

from apps.promotions.models import Promotion, Category
from apps.promotions.utils.mixins import PromotionsMixin
from utils.breadcrumbs.types import Breadcrumb
from utils.breadcrumbs.utils import reverse_bc
from utils.mixins import PageSettingsMixin


class PromotionListView(TemplateView, PromotionsMixin, PageSettingsMixin):
    template_name = 'promotions/promotions.html'
    viewname = 'promotions:list'


class PromotionCategoryView(DetailView, PromotionsMixin, PageSettingsMixin):
    template_name = 'promotions/promotions.html'
    viewname = 'promotions:category'
    initial_breadcrumbs = [reverse_bc(view=PromotionListView)]

    model = Category
    slug_field = 'url'
    slug_url_kwarg = 'category_url'

    def get_current_breadcrumb(self):
        return [Breadcrumb(self.object.name, '#')]

    def get_promotions_queryset(self):
        queryset = super().get_promotions_queryset()
        return queryset.filter(categories__url__exact=self.object.url)

    def get_ceo_context(self) -> Dict[str, Any]:
        context = super().get_ceo_context()
        context.update({'category': self.object.name})
        return context


class PromotionView(DetailView, PromotionsMixin, PageSettingsMixin):
    # DetailView
    template_name = 'promotions/promotion.html'
    model = Promotion
    slug_field = 'url'
    slug_url_kwarg = 'promotion_url'
    context_object_name = 'promotion'

    # PromotionsMixin
    promotions_max = 5
    promotions_context_name = 'other_promotions'

    # PageSettingsMixin
    viewname = 'promotions:promotion'
    initial_breadcrumbs = [reverse_bc(PromotionListView)]

    def get_current_breadcrumb(self):
        return [Breadcrumb(self.object.title, reverse('promotions:promotion', args=(self.object.url,)))]

    def get_ceo_context(self) -> Dict[str, Any]:
        context = super().get_ceo_context()
        context.update({'promotion': self.get_object().title})
        return context

    # PromotionsMixin
    def get_promotions_exclude_kwargs(self) -> Dict[str, Any]:
        return {'id': self.object.id}
