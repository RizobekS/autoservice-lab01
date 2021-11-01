from typing import Any

from django import template
from django.urls import reverse, NoReverseMatch

from apps.news.models import Article
from apps.promotions.models import Promotion
from apps.services.models import Product, Section
from apps.services.utils.helpers import service_url

register = template.Library()


@register.simple_tag(takes_context=True)
def guess_url(context: dict, obj: Any):
    """
        Tries to guess url by obj type and properties
    """
    request = context.get('request')
    if request is None:
        raise ValueError('Usage of guess_url template tag requires request in context')

    if isinstance(obj, Article):
        return reverse('knowledge_base:article', args=(obj.url,))
    elif isinstance(obj, Promotion):
        return reverse('promotions:promotion', args=(obj.url,))
    elif isinstance(obj, Product) or isinstance(obj, Section):
        return service_url(request, obj)
    else:
        raise NoReverseMatch(f'Could not find reverse for obj of type {type(obj)}')
