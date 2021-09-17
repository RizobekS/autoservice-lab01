from typing import Any, Dict

from django.views.generic import TemplateView

from apps.about.models import EditorContent
from apps.masters.utils.mixins import MastersMixin
from apps.promotions.models import Promotion
from apps.promotions.utils.mixins import PromotionsMixin
from apps.services.models import Product
from utils.mixins import PageSettingsMixin


class AboutView(TemplateView, PromotionsMixin, MastersMixin, PageSettingsMixin):
    template_name = 'about/about.html'
    viewname = 'about:about'

    promotions_max = 4
    promotions_queryset = Promotion.objects.filter(show_at_homepage=True)

    masters_additional_kwargs = {'show_at_homepage': True}

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        objects = EditorContent.objects.all()
        kwargs.update({item.key: item.text for item in objects})
        # Add product_promotions to promotions list at homepage
        kwargs['product_promotions'] = Product.objects.filter(show_in_promotions=True, active=True)
        return super().get_context_data(**kwargs)
