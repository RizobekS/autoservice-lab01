import re

from django import template
from django.template import Template, Context
from django.utils.safestring import mark_safe

from utils.car_filter import get_car_filter

register = template.Library()

spaces_regex = re.compile(r'[ ]{2,}')


@register.simple_tag(takes_context=True)
def render_with_car_context(context, text: str):
    """
        Renders given text with car_filter context variables
    """
    request = context.get('request')
    if request is None:
        raise ValueError('Usage of render_with_car_context template tag requires request in context')

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

    text_template = Template(f'{{% autoescape off %}}{text}{{% endautoescape %}}')
    result = text_template.render(Context(car_context))
    result = spaces_regex.sub(' ', result).replace(' ,', ',').replace(' .', '.')
    return mark_safe(result)
