from typing import Union

from django.http import HttpRequest
from django.urls import reverse

from apps.services.models import Section, Product
from utils.car_filter import get_car_filter


def service_url(request: HttpRequest, obj: Union[Section, Product], skip_car=False) -> str:
    args = [obj.url]
    if isinstance(obj, Section):
        viewname = 'services:section'
    elif isinstance(obj, Product):
        viewname = 'services:product'
    else:
        raise ValueError(f'Object type must be either Section or Product, {type(obj)} was given')

    car = get_car_filter(request) if not skip_car else None
    if car:
        viewname += '_car'
        args.append(car.url_args())

    return reverse(viewname, args=args)
