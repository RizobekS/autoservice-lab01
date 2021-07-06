from django import template

register = template.Library()


@register.inclusion_tag('chunks/partials/fields/hidden-next.html', takes_context=True)
def hidden_next_field(context):
    """
        Renders hidden field with value of request.GET.next if it exists, empty string otherwise
    """

    request = context.get('request')
    if request is None:
        raise ValueError('Usage of redirect_url template tag requires request in context')

    return {'GET': request.GET}


@register.inclusion_tag('chunks/partials/fields/form-hidden-fields.html')
def hidden_fields(form):
    """
        Renders all form hidden fields
    """
    return {'form': form}
