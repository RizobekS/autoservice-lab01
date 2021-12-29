from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView

from utils.car_filter import set_car_filter, get_car_filter
from utils.opengraph import OpengraphMixin
from utils.opengraph.utils import og_image
from .models import *
from .utils.mixins import CarFilterPageSettingsMixin
from ..services.models import Section, Product, CarPack


class CarView(TemplateView, CarFilterPageSettingsMixin, OpengraphMixin):
    template_name = 'cars/car.html'

    # #### CarFilterPageSettingsMixin ####

    viewname = 'cars:car'
    car_filter_context_name = 'car'

    def get_og_tags(self, **kwargs) -> dict:
        meta_context = super(CarFilterPageSettingsMixin, self).as_context()

        kwargs.update({
            'og:title': meta_context['page_title'],
            'og:description': meta_context['meta_description'],
            **og_image(self.request, self.car_filter.vendor.logo),
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
        if self.car_filter.year:
            kwargs['cars__year'] = self.car_filter.year
            if self.car_filter.modification:
                kwargs['cars'] = self.car_filter.modification
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
    """
        Data with chosen vendor, model, year and modification is received.
        According to this data response JSON is generated
    """

    # Get ID of row or None. Note: ID cannot be zero
    vendor_id = int(request.POST.get('vendor')) if request.POST.get('vendor') else None
    model_id = int(request.POST.get('model')) if request.POST.get('model') else None
    year_id = int(request.POST.get('year')) if request.POST.get('year') else None
    modification_id = int(request.POST.get('modification')) if request.POST.get('modification') else None

    # Render link for Submit button. Note: Home url is a placeholder and never should be used.
    vendor = Vendor.objects.filter(id=vendor_id, active=True).first()
    model = Model.objects.filter(id=model_id, vendor=vendor, active=True).first()
    year = Year.objects.filter(id=year_id, model=model).first()
    modification = Modification.objects.filter(id=modification_id, year=year).first()

    # Try to apply car_filter's values if form is empty
    car_filter = get_car_filter(request)
    if car_filter and not vendor and not model and not year and not modification:
        vendor = car_filter.vendor
        model = car_filter.model
        year = car_filter.year
        modification = car_filter.modification

    if vendor and model and year and modification:
        if request.user.is_authenticated:
            car_filter, created = CarFilter.objects.get_or_create(user=request.user, vendor=vendor, model=model, year=year, modification=modification)
            if not created:
                car_filter.update_last_used()
        else:
            car_filter = CarFilter.objects.create(vendor=vendor, model=model, year=year, modification=modification)
        set_car_filter(request, car_filter)

        # Construct reverse url according to url_args[] and view_name hidden fields values and selected car
        viewname = request.POST.get('view_name')
        args = request.POST.getlist('url_args[]')
        args.append(car_filter.url_args())
        url = reverse(viewname, args=args)

    else:
        url = reverse('home:index')

    # Retrieve options
    vendor_set = [{'value': item.id, 'label': item.name, 'selected': vendor == item} for item in Vendor.objects.filter(active=True)]
    model_set = [{'value': item.id, 'label': item.name, 'selected': model == item} for item in Model.objects.filter(vendor=vendor, active=True)] if vendor else []
    year_set = [{'value': item.id, 'label': item.name, 'selected': year == item} for item in Year.objects.filter(model=model)] if model else []
    modification_set = [{'value': item.id, 'label': item.name, 'selected': modification == item} for item in Modification.objects.filter(year=year)] if year else []

    # Insert model names at the beginning
    vendor_set.insert(0, {'value': '', 'label': Vendor._meta.verbose_name, 'selected': not vendor, 'placeholder': True})
    model_set.insert(0, {'value': '', 'label': Model._meta.verbose_name, 'selected': not model, 'placeholder': True})
    year_set.insert(0, {'value': '', 'label': Year._meta.verbose_name, 'selected': not year, 'placeholder': True})
    modification_set.insert(0, {'value': '', 'label': Modification._meta.verbose_name, 'selected': not modification, 'placeholder': True})

    data = {
        'vendor': vendor_set,
        'model': model_set,
        'year': year_set,
        'modification': modification_set,
        'url': url,
    }

    return JsonResponse(data)
