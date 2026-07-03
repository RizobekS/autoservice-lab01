from typing import Union

from django import template

from apps.knowledge_base.models import Symptom, FaqEntry
from apps.masters.models import Master
from apps.news.models import Article
from apps.promotions.models import Promotion
from apps.services.models import Product

register = template.Library()


@register.simple_tag
def template_name(obj: Union[Article, Promotion, Master]) -> str:
    """
        Determines type of object passed and returns corresponding template_name
    """
    folder = 'tags/chunks/'

    if isinstance(obj, Article):
        name = 'new_article.html'
    elif isinstance(obj, Promotion):
        name = 'new_promotion.html'
    elif isinstance(obj, Product):
        name = 'new_product.html'
    elif isinstance(obj, Symptom):
        name = 'new_symptom.html'
    elif isinstance(obj, FaqEntry):
        name = 'new_faq_entry.html'
    else:
        raise ValueError(f'obj must be instance of Article, Promotion or Master, got {type(obj)} instead')

    return folder + name
