import re

from django import template
from django.template import Template, Context
from django.utils.safestring import mark_safe

register = template.Library()

spaces_regex = re.compile(r'[ ]{2,}')


@register.simple_tag()
def render_with_context(text: str, *args, library: str = '', **kwargs):
    """
        Renders given text with computed context (context is made of args and kwargs)
    :param text: The text will be rendered with computed context
    :param args: Each positional argument having dictionary type will be added to the context
    :param kwargs: All keyword arguments are added as context, except 'templatetags'
    :param library: A library name, that will be loaded at beginning of rendered text (only one library can be added)
    :return: Safe html string
    """

    # Construct context
    context = {}
    for passed_context in args:
        if isinstance(passed_context, dict):
            context.update(passed_context)
    context.update(kwargs)

    # Get library to be appended, if there are
    library = f'{{% load {library} %}}' if library else library

    text_template = Template(f'{library}{{% autoescape off %}}{text}{{% endautoescape %}}')
    result = text_template.render(Context(context))
    result = spaces_regex.sub(' ', result).replace(' ,', ',').replace(' .', '.')
    return mark_safe(result)
