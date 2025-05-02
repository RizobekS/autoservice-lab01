from django import template
from django.urls import ResolverMatch
from django.utils.safestring import mark_safe

from utils.helpers import hidden_field_tag
from utils.car_filter import get_car_filter

register = template.Library()

@register.simple_tag(takes_context=True)
def redirect_url(context: dict):
    request = context.get('request')
    if request is None:
        raise ValueError('Usage of redirect_url template tag requires request in context')

    resolver: ResolverMatch = request.resolver_match
    html = []
    CAR_SUFFIX = '_car'

    car = get_car_filter(request)

    # Redirect to section/product with given car values
    if 'services' in resolver.namespaces:
        if resolver.kwargs.get('section_url'):
            html.append(hidden_field_tag('url_args[]', resolver.kwargs.get('section_url')))
        if resolver.kwargs.get('product_url'):
            html.append(hidden_field_tag('url_args[]', resolver.kwargs.get('product_url')))
        if car:
            for part in car.url_args():
                html.append(hidden_field_tag('url_args[]', part))
        view_name = resolver.view_name if resolver.view_name.endswith(CAR_SUFFIX) else resolver.view_name + CAR_SUFFIX
    else:
        view_name = 'cars:car'
        if car:
            for part in car.url_args():
                html.append(hidden_field_tag('url_args[]', part))

    html.append(hidden_field_tag('view_name', view_name))

    return mark_safe('\n'.join(html))
