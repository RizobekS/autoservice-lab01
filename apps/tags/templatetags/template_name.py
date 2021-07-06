from typing import Union

from django import template

from apps.masters.models import Master
from apps.news.models import Article
from apps.promotions.models import Promotion

register = template.Library()


@register.simple_tag
def template_name(obj: Union[Article, Promotion, Master]) -> str:
    """
        Determines type of object passed and returns corresponding template_name
    """
    folder = 'tags/chunks/'

    if isinstance(obj, Article):
        name = 'article.html'
    elif isinstance(obj, Promotion):
        name = 'promotion.html'
    elif isinstance(obj, list):
        name = 'master.html'
    else:
        raise ValueError(f'obj must be instance of Article, Promotion or Master, got {type(obj)} instead')

    return folder + name
