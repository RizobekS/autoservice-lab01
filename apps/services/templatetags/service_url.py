from typing import Union

from django import template

from apps.services.models import Section, Product
from apps.services.utils import helpers

register = template.Library()

@register.simple_tag(takes_context=True)
def service_url(context: dict, obj: Union[Section, Product]) -> str:
    """
        Template tag wrapper for helpers.service_url() function.
        Used for getting particular service url with car url args if needed.
    """

    request = context.get('request')
    if request is None:
        raise ValueError('Usage of service_url template tag requires request in context')

    return helpers.service_url(request, obj)
