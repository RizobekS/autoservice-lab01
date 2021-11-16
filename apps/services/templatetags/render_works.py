from typing import Union

from django import template
from django.template import Context
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag(takes_context=True)
def works(context: Union[Context, dict]):
    """
        Renders services/chunks/works.html template with external context
    """
    context = context.flatten() if isinstance(context, Context) else context
    return render_to_string('services/chunks/works.html', context=context)
