from typing import Any, Dict

from django.views.generic import DetailView, TemplateView

from apps.promotions.models import Promotion
from apps.promotions.utils.mixins import PromotionsMixin
from apps.site_settings.utils.mixins import MetaTagsMixin
from utils.breadcrumbs.mixins import PageTitleMixin
from utils.breadcrumbs.utils import reverse_bc


class PromotionListView(TemplateView, PromotionsMixin, PageTitleMixin, MetaTagsMixin):
    template_name = 'promotions/promotions.html'
    page_title = 'Акции'
    viewname = 'promotions:list'


class PromotionView(DetailView, PromotionsMixin, PageTitleMixin, MetaTagsMixin):
    # DetailView
    template_name = 'promotions/promotion.html'
    model = Promotion
    slug_field = 'url'
    slug_url_kwarg = 'promotion_url'
    context_object_name = 'promotion'

    # PromotionsMixin
    promotions_max = 5
    promotions_context_name = 'other_promotions'

    # MetaTagsMixin
    meta_tags_key = 'promotions:promotion'

    # PageTitleMixin
    initial_breadcrumbs = [reverse_bc(PromotionListView)]

    # PromotionsMixin
    def get_promotions_exclude_kwargs(self) -> Dict[str, Any]:
        return {'id': self.object.id}

    # PageTitleMixin
    def get_page_title(self):
        return self.object.title

    # MetaTagsMixin
    def get_meta_context(self) -> Dict[str, Any]:
        return {'promotion': self.get_page_title()}
