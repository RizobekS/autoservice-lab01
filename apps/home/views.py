from django.views.generic import TemplateView

from apps.cars.utils.mixins import VendorsMixin
from apps.masters.utils.mixins import MastersMixin
from apps.promotions.models import Promotion
from apps.promotions.utils.mixins import PromotionsMixin
from apps.services.models import Product, Section
from apps.services.utils.mixins import ProductsMixin, SectionsMixin
from apps.site_settings.utils.mixins import CEOMixin


class IndexView(TemplateView, PromotionsMixin, VendorsMixin, MastersMixin, ProductsMixin, SectionsMixin, CEOMixin):
    template_name = 'home/index.html'

    ceo_key = 'home:index'

    promotions_max = 4
    promotions_queryset = Promotion.objects.filter(show_at_homepage=True)

    masters_additional_kwargs = {'show_at_homepage': True}

    sections_max = 9
    sections_queryset = Section.objects.filter(show_at_homepage=True)

    def get_sections(self):
        queryset = list(super().get_sections_queryset().all())
        queryset = sorted(queryset, key=lambda item: item.level())
        return queryset

    products_max = 9
    products_queryset = Product.objects.filter(show_at_homepage=True)

    # Add product_promotions to promotions list at homepage
    def get_context_data(self, **kwargs):
        kwargs['product_promotions'] = Product.objects.filter(show_in_promotions=True, active=True)
        return super().get_context_data(**kwargs)
