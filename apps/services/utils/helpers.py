from typing import Union

from django.http import HttpRequest
from django.urls import reverse

from apps.services.models import Section, Product
from utils.car_filter import get_car_filter


def service_url(request: HttpRequest, obj: Union[Section, Product], skip_car=False) -> str:
    if isinstance(obj, Section):
        viewname = 'services:section'
        args = [obj.url]
    elif isinstance(obj, Product):
        viewname = 'services:product'
        args = [obj.section.url, obj.url]
    else:
        raise ValueError(f'Object type must be either Section or Product, {type(obj)} was given')

    car = get_car_filter(request) if not skip_car else None
    if car:
        viewname += '_car'
        args.append(car.url_args())

    return reverse(viewname, args=args)


"""
    vvvvvvv UNUSED STUFF vvvvvvv
"""
# def service_breadcrumbs(request, obj: Union[Section, Product]) -> list:
#     section = obj if isinstance(obj, Section) else obj.section
#     viewname = 'services:section'
#
#     args = (section.url,)
#     breadcrumbs = [Breadcrumb(section.title, reverse(viewname, args=args))]
#     temp_section = section
#     while temp_section.parent_section:
#         temp_section = temp_section.parent_section
#         args = (temp_section.url,)
#         bc = Breadcrumb(temp_section.title, reverse(viewname, args=args))
#         breadcrumbs.append(bc)
#     breadcrumbs = breadcrumbs[::-1]
#
#     if isinstance(obj, Product):
#         viewname = 'services:product'
#         args = (section.url, obj.url)
#         bc = Breadcrumb(obj.title, reverse(viewname, args=args))
#         breadcrumbs.append(bc)
#
#     car_filter = get_car_filter(request)
#
#     if car_filter:
#         viewname += '_car'
#
#         bc = Breadcrumb(car_filter.vendor.name, reverse(viewname, args=(*args, car_filter.vendor.url_args(),)))
#         breadcrumbs.append(bc)
#         if car_filter.model:
#             bc = Breadcrumb(car_filter.model.name, reverse(viewname, args=(*args, car_filter.model.url_args(),)))
#             breadcrumbs.append(bc)
#             if car_filter.year:
#                 if car_filter.modification:
#                     name = f'{car_filter.year.name} {car_filter.modification.name}'
#                     url_args = car_filter.modification.url_args()
#                 else:
#                     name = car_filter.year.name
#                     url_args = car_filter.year.url_args()
#                 bc = Breadcrumb(name, reverse(viewname, args=(*args, url_args)))
#                 breadcrumbs.append(bc)
#
#     return breadcrumbs
#
# def service_page_title(request, obj: Union[Section, Product]) -> str:
#     car = get_car_filter(request)
#     if car:
#         return f'{obj.title} {car.full_name()}'
#     else:
#         return obj.title
