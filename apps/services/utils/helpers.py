from typing import Union

from django.http import HttpRequest
from django.urls import reverse

from apps.services.models import Section, Product
from utils.car_filter import get_car_filter


SECTIONS_WITHOUT_CAR_LINKS = ('shinnyi-centr', 'detailing')


def service_url(request: HttpRequest, obj: Union[Section, Product], skip_car=False) -> str:
    args = [obj.url]
    if isinstance(obj, Section):
        viewname = 'services:section'
    elif isinstance(obj, Product):
        viewname = 'services:product'
    else:
        raise ValueError(f'Object type must be either Section or Product, {type(obj)} was given')

    section_without_car = (
        isinstance(obj, Section)
        and obj.url in SECTIONS_WITHOUT_CAR_LINKS
    )
    car = get_car_filter(request) if not skip_car and not section_without_car else None
    if car and not obj.canonical_to_original:
        viewname += '_car'
        args.append(car.url_args())

    return reverse(viewname, args=args)
