from django import template
from django.db.models import QuerySet

register = template.Library()


@register.filter
def merge(queryset1: QuerySet, queryset2: QuerySet):
    """
        Merges two querysets in a single list
    """
    return list(queryset1) + list(queryset2)
