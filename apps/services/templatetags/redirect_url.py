from django import template
from django.urls import ResolverMatch
from django.utils.safestring import mark_safe

from utils.helpers import hidden_field_tag

register = template.Library()

@register.simple_tag(takes_context=True)
def redirect_url(context: dict):
    """
        Adds hidden fields with viewname and url args to ajax form.
        These fields are used by ajax_filter function to construct url to redirect to.
    """

    request = context.get('request')
    if request is None:
        raise ValueError('Usage of redirect_url template tag requires request in context')

    resolver: ResolverMatch = request.resolver_match

    html = []

    # Redirect to section/product with given car values
    if 'services' in resolver.namespaces:
        if resolver.kwargs.get('section_url'):
            html.append(hidden_field_tag('url_args[]', resolver.kwargs.get('section_url')))
        if resolver.kwargs.get('product_url'):
            html.append(hidden_field_tag('url_args[]', resolver.kwargs.get('product_url')))
        html.append(hidden_field_tag('view_name', resolver.view_name))
    else:
        view_name = 'cars:car'
        html.append(hidden_field_tag('view_name', view_name))

    return mark_safe('\n'.join(html))
