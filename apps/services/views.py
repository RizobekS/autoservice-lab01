from django.shortcuts import render

from utils.car_filter import set_car_filter, remove_car_filter
from utils.shortcuts import exists_or_404
from .models import Section, Product
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
        car_filter = urls.save(request)
        set_car_filter(request, car_filter)
    else:
        remove_car_filter(request)
        car_filter = None

    # Render breadcrumbs
    breadcrumbs = service_breadcrumbs(request, current_section)

    context = {
        'current_section': current_section,
        'child_sections': child_sections if child_sections.exists() else None,

        'page_title': service_page_title(request, current_section),
        'selected_car': car_filter and car_filter.is_full(),
        'breadcrumbs': breadcrumbs,
        'bg_object': current_section,
    }

    return render(request, 'services/section.html', context)


def product_view(request, section_url: str, product_url: str, urls: CarUrls = None):
    # Find current section and product
    current_section = Section.objects.filter(url=section_url, active=True)
    current_section: Section = exists_or_404(current_section, f'Section with url={section_url} does not exist')
    product = Product.objects.filter(url=product_url, active=True, section=current_section)
    product: Product = exists_or_404(product, f'Product with url={product_url} and section={current_section} does not exist')

    # Renew car filter if urls provided or try to get existing one
    if urls:
        car_filter = urls.save(request)
        set_car_filter(request, car_filter)
    else:
        remove_car_filter(request)
        car_filter = None

    # Render breadcrumbs
    breadcrumbs = service_breadcrumbs(request, product)

    context = {
        'product': product,
        'current_section': current_section,
        'other_products': current_section.product_set.exclude(id=product.id),

        'page_title': service_page_title(request, product),
        'selected_car': car_filter and car_filter.is_full(),
        'breadcrumbs': breadcrumbs,
        'bg_object': product,
    }

    return render(request, 'services/product.html', context)

