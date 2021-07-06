from django import template

from utils.helpers import format_price

register = template.Library()


@register.filter
def pretty_price(number: float):
    return format_price(number)
