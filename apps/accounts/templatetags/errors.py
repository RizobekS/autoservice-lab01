from django import template

register = template.Library()


@register.inclusion_tag('chunks/partials/errors/non-field.html')
def non_field_errors(form):
    """
        Renders NON field errors in <small class="text-warning"></small> tags
    """
    return {'form': form}


@register.inclusion_tag('chunks/partials/errors/field.html')
def field_errors(field):
    """
        Renders field errors in <small class="text-warning"></small> tags
    """
    return {'field': field}
