from django.shortcuts import render

from .models import Section, Product
from utils.helpers import exists_or_404, get_car_filter, set_car_filter
from .utils.helpers import service_breadcrumbs, service_page_title
from ..cars.utils.types import CarUrls


def section_view(request, section_url: str, urls: CarUrls = None):
    # Find current section
    current_section = Section.objects.filter(url=section_url, active=True)
    current_section: Section = exists_or_404(current_section)

    # Retrieve child sections
    child_sections = Section.objects.filter(active=True, parent_section=current_section)

    # Renew car filter if urls provided or try to get existing one
    if urls:
        car_filter = urls.save()
        set_car_filter(request, car_filter, True)
    else:
        car_filter = get_car_filter(request)

    # Render breadcrumbs
    breadcrumbs = service_breadcrumbs(request, current_section)

    context = {
        'current_section': current_section,
        'child_sections': child_sections if child_sections.exists() else None,
        'services': True,  # Is used to include proper header parts

        'service_page_title': service_page_title(request, current_section),
        'selected_car': car_filter and car_filter.is_full(),
        'breadcrumbs': breadcrumbs,
    }

    return render(request, 'services/section.html', context)


def product_view(request, section_url: str, product_url: str, urls: CarUrls):
    # Find current section and product
    current_section = Section.objects.filter(url=section_url, active=True)
    current_section: Section = exists_or_404(current_section)
    product = Product.objects.filter(url=product_url, active=True, section=current_section)
    product: Product = exists_or_404(product)

    # Renew car filter if urls provided or try to get existing one
    if urls:
        car_filter = urls.save()
        set_car_filter(request, car_filter, True)
    else:
        car_filter = get_car_filter(request)

    # Render breadcrumbs
    breadcrumbs = service_breadcrumbs(request, product)

    context = {
        'product': product,
        'current_section': current_section,
        'other_products': current_section.product_set.exclude(id=product.id),
        'services': True,  # Is used to include proper header parts

        'service_page_title': service_page_title(request, current_section),
        'selected_car': car_filter and car_filter.is_full(),
        'breadcrumbs': breadcrumbs,
    }

    return render(request, 'services/product.html', context)

