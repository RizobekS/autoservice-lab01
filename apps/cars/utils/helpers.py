from django.urls import reverse

from apps.cars.models import CarFilter
from utils.breadcrumbs.types import Breadcrumb


def car_breadcrumbs(car_filter: CarFilter) -> list:
    breadcrumbs = []

    bc = Breadcrumb(car_filter.vendor.name, reverse('cars:car', args=(car_filter.vendor.url_args(),)))
    breadcrumbs.append(bc)
    if car_filter.model:
        bc = Breadcrumb(car_filter.model.name, reverse('cars:car', args=(car_filter.model.url_args(),)))
        breadcrumbs.append(bc)

    return breadcrumbs

def car_page_title(car_filter: CarFilter) -> str:
    return f'Сервисное обслуживание {car_filter.full_name()}'
