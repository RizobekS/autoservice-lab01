from pathlib import Path
from typing import Optional

from django.http import Http404, HttpRequest
from django.templatetags.static import static

from apps.cars.models import CarFilter

ADMIN_EXAMPLES_ROOT = Path('images') / 'admin-examples'

def admin_example(image_name: str, name: str = 'Посмотреть'):
    link = static(str(ADMIN_EXAMPLES_ROOT / image_name))
    return link_tag(link, name, True, 'font-weight: bold; text-decoration: underline;')

def link_tag(link: str, name: str = None, target_blank=False, style=''):
    target_blank = 'target="_blank"' if target_blank else ''
    style = f'style="{style}"' if style else style
    return f'<a {target_blank} href="{link}" {style}>{name if name else link}</a>'

def hidden_field_tag(name: str, url: str) -> str:
    return f'<input type="hidden" name="{name}" value="{url}"/>'

def format_price(number: float, currency: str = None) -> str:
    decimal, fractional = str(number).split('.')
    decimal = decimal[::-1]
    price = " ".join([decimal[i:i + 3] for i in range(0, len(decimal), 3)])[::-1]
    price = f'{price}.{fractional}'
    return f'{price}{currency}' if currency else price


def exists_or_404(query_set):
    if query_set.exists():
        return query_set.first()
    else:
        raise Http404()


_FILTER_HASH = 'car_filter'

def get_car_filter(request: HttpRequest) -> Optional[CarFilter]:
    """
        Returns CarFilter object saved in session if it exists and None otherwise
    """
    filter_id = request.session.get(_FILTER_HASH, None)
    if filter_id is None:
        return None
    car_filter = CarFilter.objects.filter(id=filter_id)
    return car_filter.first() if car_filter.exists() else None

def set_car_filter(request: HttpRequest, filter_obj: CarFilter, delete_old: bool = False) -> None:
    """
        Deletes previous CarFilter object if it exists, sets the new one and returns it back
    """
    if delete_old and _FILTER_HASH in request.session:
        CarFilter.objects.filter(id=request.session[_FILTER_HASH]).delete()
    request.session[_FILTER_HASH] = filter_obj.id

def remove_car_filter(request: HttpRequest):
    """
        Deletes current CarFilter object if it exists
    """
    if _FILTER_HASH in request.session:
        CarFilter.objects.filter(id=request.session[_FILTER_HASH]).delete()
        del request.session[_FILTER_HASH]
