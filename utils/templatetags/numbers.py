from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg


@register.filter
def mod(value, arg):
    return value % arg
