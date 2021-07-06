from typing import Any, Dict

from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView

from apps.promotions.models import Promotion
from apps.promotions.utils.mixins import PromotionsMixin
from utils.breadcrumbs.mixins import PageTitleMixin
from utils.breadcrumbs.types import Breadcrumb


class PromotionListView(TemplateView, PromotionsMixin, PageTitleMixin):
    template_name = 'promotions/promotions.html'
    page_title = 'Акции'


class PromotionView(DetailView, PromotionsMixin, PageTitleMixin):
    # DetailView
    template_name = 'promotions/promotion.html'
    model = Promotion
    slug_field = 'url'
    slug_url_kwarg = 'promotion_url'
    context_object_name = 'promotion'

    # DetailView
    promotions_max = 5
    promotions_context_name = 'other_promotions'

    # PageTitleMixin
    initial_breadcrumbs = [Breadcrumb('Акции', reverse_lazy('promotions:list'))]

    # PromotionsMixin
    def get_promotions_exclude_kwargs(self) -> Dict[str, Any]:
        return {'id': self.object.id}

    # PageTitleMixin
    def get_page_title(self):
        return self.object.title
