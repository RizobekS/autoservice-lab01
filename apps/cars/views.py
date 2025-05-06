from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse, NoReverseMatch
from django.views.generic import TemplateView, RedirectView

from utils.car_filter import set_car_filter, get_car_filter
from utils.opengraph import OpengraphMixin
from utils.opengraph.utils import og_image
from .models import *
from .utils.mixins import CarFilterPageSettingsMixin
from .utils.types import CarUrls
from ..services.models import Section, Product, CarPack


class RedirectOldCarUrls(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        urls: CarUrls = kwargs.get('urls')
        new_car_urls = '/'.join([urls.vendor, urls.model])
        return reverse('cars:car', args=[new_car_urls])

class CarView(TemplateView, CarFilterPageSettingsMixin, OpengraphMixin):
    template_name = 'cars/car.html'

    # #### CarFilterPageSettingsMixin ####

    viewname = 'cars:car'
    car_filter_context_name = 'car'

    def get_og_tags(self, **kwargs) -> dict:
        meta_context = super(CarFilterPageSettingsMixin, self).as_context()
        if self.car_filter.model and self.car_filter.model.header_image:
            image_field = self.car_filter.model.header_image
        elif self.car_filter.vendor.header_image:
            image_field = self.car_filter.vendor.header_image
        else:
            image_field = self.car_filter.vendor.logo

        kwargs.update({
            'og:title': meta_context['page_title'],
            'og:description': meta_context['meta_description'],
            **og_image(self.request, image_field),
            'og:url': self.request.build_absolute_uri(self.request.path),
        })
        return super().get_og_tags(**kwargs)

    def get_current_breadcrumb(self):
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.car_filter.model:  # Only for cars with model selected (and higher)
            extra_context = self._root_section_products()
        else:  # Only for vendors
            extra_context = self._root_sections()

        context.update(extra_context)
        return context

    def _root_section_products(self):
        # Find all car_pack's that include current car_filter
        kwargs = {'cars__year__model__vendor': self.car_filter.vendor,
                  'cars__year__model': self.car_filter.model}
        car_packs = CarPack.objects.filter(**kwargs)

        products = list(Product.objects.filter(active=True).filter(Q(car_pack__in=car_packs) | Q(car_pack__isnull=True)))
        root_sections = {}
        for product in products:
            root = product.root_section()

            # Skip products from 'others' section with canonical_to_original=True
            if root.url == 'others' and product.canonical_to_original:
                continue

            if root in root_sections:
                if len(root_sections[root]) < 5:
                    root_sections[root].add(product)
            else:
                root_sections[root] = {product}  # Creating set
        root_sections = dict(sorted(root_sections.items(), key=lambda x: x[0].sorting))
        return {'root_sections': root_sections}

    @staticmethod
    def _root_sections():
        return {'sections': Section.objects.filter(active=True, parent_section=None)}


def ajax_filter(request):
    vendor_id = int(request.POST.get('vendor')) if request.POST.get('vendor') else None
    model_id = int(request.POST.get('model')) if request.POST.get('model') else None

    vendor = Vendor.objects.filter(id=vendor_id, active=True).first()
    model = Model.objects.filter(id=model_id, vendor=vendor, active=True).first()

    car_filter = get_car_filter(request)
    if car_filter and not vendor and not model:
        vendor = car_filter.vendor
        model = car_filter.model

    if vendor and model:
        if request.user.is_authenticated:
            car_filter, created = CarFilter.objects.get_or_create(
                user=request.user,
                vendor=vendor,
                model=model,
                year=None,
                modification=None
            )
            if not created:
                car_filter.update_last_used()
        else:
            car_filter = CarFilter.objects.create(
                vendor=vendor,
                model=model,
                year=None,
                modification=None
            )
        set_car_filter(request, car_filter)

        viewname = request.POST.get('view_name')
        args = request.POST.getlist('url_args[]')

        # Удаляем пустые элементы и None
        args = [arg for arg in args if arg not in (None, '', 'None')]

        # Добавляем аргументы из car_filter
        args.extend(filter(None, car_filter.url_args()))  # удалит None из кортежа

        # Проверяем, что viewname не None и существует такой маршрут
        if viewname and args:
            try:
                url = reverse(viewname, args=args)
            except NoReverseMatch:
                url = reverse('home:index')
        else:
            url = reverse('home:index')
    else:
        url = reverse('home:index')

    vendor_set = [{'value': item.id, 'label': item.name, 'selected': vendor == item} for item in Vendor.objects.filter(active=True)]
    model_set = [{'value': item.id, 'label': item.name, 'selected': model == item} for item in Model.objects.filter(vendor=vendor, active=True)] if vendor else []

    vendor_set.insert(0, {'value': '', 'label': Vendor._meta.verbose_name, 'selected': not vendor, 'placeholder': True})
    model_set.insert(0, {'value': '', 'label': Model._meta.verbose_name, 'selected': not model, 'placeholder': True})

    data = {
        'vendor': vendor_set,
        'model': model_set,
        'url': url,
    }

    return JsonResponse(data)
