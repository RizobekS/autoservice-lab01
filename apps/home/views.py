from django.views.generic import TemplateView

from apps.cars.utils.mixins import VendorsMixin
from apps.home.models import Slide
from apps.masters.utils.mixins import MastersMixin
from apps.promotions.models import Promotion
from apps.promotions.utils.mixins import PromotionsMixin
from apps.services.models import Product, Section
from apps.services.utils.mixins import ProductsMixin, SectionsMixin
from apps.site_settings.utils.mixins import CEOMixin
from apps.work_gallery.models import Work, Category
from apps.news.models import Article
from apps.news.utils.mixins import LatestArticlesMixin
from apps.accounts.forms import AppointmentForm
from utils.car_filter import get_car_filter


class IndexView(TemplateView, PromotionsMixin, VendorsMixin, MastersMixin, ProductsMixin, SectionsMixin, CEOMixin, LatestArticlesMixin):
    template_name = 'home/new_home.html'

    ceo_key = 'home:index'

    promotions_max = 4
    promotions_queryset = Promotion.objects.filter(show_at_homepage=True)

    masters_max = 4
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

        request = self.request

        if request.user.is_authenticated and request.user.carfilter_set.exists():
            car = request.user.carfilter_set.select_related(
                'vendor',
                'model__vendor',
                'year__model__vendor',
                'modification__year__model__vendor'
            ).latest()
        else:
            car = get_car_filter(request)

        initial = {
            'full_name': request.user.get_full_name() if request.user.is_authenticated else '',
            'car': car.full_name() if car else '',
        }


        kwargs['appointment_form'] = AppointmentForm(initial=initial)
        kwargs['product_promotions'] = Product.objects.filter(show_in_promotions=True, active=True)
        kwargs['main_slides'] = Slide.objects.filter(active=True)
        kwargs['work_gallery_queryset'] = Work.objects.prefetch_related('image_set', 'categories').filter(active=True).order_by('-id')[:6]
        kwargs['categories_queryset'] = Category.objects.exclude(work=None)
        kwargs['latest_articles_queryset'] = Article.objects.filter(is_news=False)[:6]
        return super().get_context_data(**kwargs)
