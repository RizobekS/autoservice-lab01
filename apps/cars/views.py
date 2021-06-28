from django.http import JsonResponse
from django.shortcuts import render

from .models import *
from utils.helpers import set_car_filter, get_car_filter
from .utils.helpers import car_page_title, car_breadcrumbs
from .utils.types import CarUrls
from ..services.models import Section, Product


def car_view(request, urls: CarUrls):
    # Get Vendor object
    car_filter = urls.save()
    set_car_filter(request, car_filter, True)

    context = {
        'service_page_title': car_page_title(car_filter),

        'page_title': car_page_title(car_filter),
        'breadcrumbs': car_breadcrumbs(car_filter),
        'car': car_filter,
        'cars': True,  # Is used to include proper header parts
    }

    # Only for vendor-model and higher level pages
    if car_filter.model:
        # Dict of kwargs for given car_filter
        kwargs = {'cars__year__model__vendor': car_filter.vendor}
        if car_filter.model:
            kwargs['cars__year__model'] = car_filter.model
            if car_filter.year:
                kwargs['cars__year'] = car_filter.year
                if car_filter.modification:
                    kwargs['cars'] = car_filter.modification
        print('Product kwargs:', kwargs)

        products = list(Product.objects.filter(active=True, **kwargs))
        root_sections = {}
        for product in products:
            root = product.root_section()
            if root in root_sections and len(root_sections[root]) <= 5:
                root_sections[root].append(product)
            else:
                root_sections[root] = [product]

        context['root_sections'] = root_sections
    else:  # Only for vendor-level pages
        context['sections'] = Section.objects.filter(active=True, parent_section=None)

    return render(request, 'cars/car.html', context)


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
    vendor = Vendor.objects.filter(id=vendor_id).first()
    model = Model.objects.filter(id=model_id, vendor=vendor).first()
    year = Year.objects.filter(id=year_id, model=model).first()
    modification = Modification.objects.filter(id=modification_id, year=year).first()
    if vendor and model and year and modification:
        car_filter = CarFilter.objects.create(vendor=vendor, model=model, year=year, modification=modification)
        set_car_filter(request, car_filter, True)

        # Construct reverse url according to url_args[] and view_name hidden fields values and selected car
        args = request.POST.getlist('url_args[]')
        args.append(car_filter.url_args())
        url = reverse(request.POST.get('view_name'), args=args)

    else:
        url = reverse('home:index')

        # # Try to prepopulate form with information from session
        # car_filter = get_car_filter(request)
        # if car_filter:
        #     vendor = car_filter.vendor if car_filter.vendor else vendor
        #     model = car_filter.model if car_filter.model else model
        #     year = car_filter.year if car_filter.year else year
        #     modification = car_filter.modification if car_filter.modification else modification

    # Retrieve options
    vendor_set = [{'value': item.id, 'label': item.name, 'selected': vendor == item} for item in Vendor.objects.all()]
    model_set = [{'value': item.id, 'label': item.name, 'selected': model == item} for item in Model.objects.filter(vendor=vendor)] if vendor else []
    year_set = [{'value': item.id, 'label': item.name, 'selected': year == item} for item in Year.objects.filter(model=model)] if model else []
    modification_set = [{'value': item.id, 'label': item.name, 'selected': modification == item} for item in Modification.objects.filter(year=year)] if year else []

    # Insert model names at the beginning
    vendor_set.insert(0, {'label': Vendor._meta.verbose_name, 'selected': not vendor, 'placeholder': True})
    model_set.insert(0, {'label': Model._meta.verbose_name, 'selected': not model, 'placeholder': True})
    year_set.insert(0, {'label': Year._meta.verbose_name, 'selected': not year, 'placeholder': True})
    modification_set.insert(0, {'label': Modification._meta.verbose_name, 'selected': not modification, 'placeholder': True})

    data = {
        'vendor': vendor_set,
        'model': model_set,
        'year': year_set,
        'modification': modification_set,
        'url': url,
    }

    return JsonResponse(data)
