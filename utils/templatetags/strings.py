from re import sub

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@stringfilter
def break_words(string: str) -> str:
    """
        Replaces all spaces with <br/> tags
    """
    if not isinstance(string, str):
        raise ValueError(f'str value expected, got {type(string)} instead')

    ar = string.split(' ')
    return mark_safe('<br/>'.join(ar))


@register.filter
@stringfilter
def extract_phone(string: str) -> str:
    """
        Converts +998(23) 123-34-34 into +99823123-34-34
    """
    if not isinstance(string, str):
        raise ValueError(f'str value expected, got {type(string)} instead')

    return sub('[^+\\d]', '', string)
