# Create your views here.
from django.views.generic import TemplateView

from apps.cars.utils.mixins import VendorsMixin
from apps.masters.utils.mixins import MastersMixin
from apps.promotions.utils.mixins import PromotionsMixin
from apps.services.utils.mixins import ProductsMixin
from apps.site_settings.utils.mixins import MetaTagsMixin


class IndexView(TemplateView, PromotionsMixin, VendorsMixin, MastersMixin, ProductsMixin, MetaTagsMixin):
    template_name = 'home/index.html'

    meta_tags_key = 'home:index'

    promotions_max = 4
    promotions_additional_kwargs = {'show_at_homepage': True}

    masters_additional_kwargs = {'show_at_homepage': True}

    products_max = 9
    products_additional_kwargs = {'show_at_homepage': True}
