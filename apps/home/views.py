# Create your views here.
from django.views.generic import TemplateView

from apps.cars.utils.mixins import VendorsMixin
from apps.masters.utils.mixins import MastersMixin
from apps.promotions.utils.mixins import PromotionsMixin
from apps.services.utils.mixins import ProductsMixin


class IndexView(TemplateView, PromotionsMixin, VendorsMixin, MastersMixin, ProductsMixin):
    template_name = 'home/index.html'

    promotions_max = 4
    promotions_additional_kwargs = {'show_at_homepage': True}

    masters_additional_kwargs = {'show_at_homepage': True}

    products_max = 9
    products_additional_kwargs = {'show_at_homepage': True}

# def index(request):
#     promotions = Promotion.objects.filter(active=True, show_at_homepage=True)
#     vendors = Vendor.objects.filter(active=True)
#     masters = Master.objects.filter(active=True, show_at_homepage=True)
#
#     homepage_services = list(Section.objects.filter(active=True)) + list(Product.objects.filter(active=True))
#
#     context = {
#         'promotions': promotions,
#         'vendors': vendors,
#         'homepage_services': homepage_services,
#         'masters': promotions,
#     }
#
#     return render(request, 'home/index.html', context=context)
