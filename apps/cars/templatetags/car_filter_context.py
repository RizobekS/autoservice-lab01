import re

from django import template

from utils.car_filter import get_car_filter

register = template.Library()

spaces_regex = re.compile(r'[ ]{2,}')


@register.simple_tag(takes_context=True)
def get_car_filter_context(context):
    """
        Returns dictionary with dictionary of car_filter context, namely vendor, model, year, modification
    """
    request = context.get('request')
    if request is None:
        raise ValueError('Usage of get_car_filter_context template tag requires request in context')

    car = get_car_filter(request)

    if car:
        car_context = {
            'vendor': car.vendor.name if car.vendor else '',
            'model': car.model.name if car.model else '',
            'year': car.year.name if car.year else '',
            'modification': car.modification.name if car.modification else '',
        }
    else:
        car_context = {}

    return car_context
