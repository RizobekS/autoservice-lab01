from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def is_active(context: dict, namespace: str):
    """
        Returns class="active" if resolver.namespace is equal to passed string and "" otherwise
    """
    request = context.get('request')
    if request is None:
        raise ValueError('Usage of is_active template tag requires request in context')

    return mark_safe('class="active"' if request.resolver_match.namespace == namespace else '')
