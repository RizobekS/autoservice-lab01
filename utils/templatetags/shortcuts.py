from django import template

register = template.Library()


@register.simple_tag
def choose(condition, value1: str, value2: str = ''):
    """
        {% if_ cond 'This_will_be_returned_if_true' 'This_will_be_returned_if_false' %}
        {% if_ cond 'This_will_be_returned_if_true' %}  Empty string will be returned if false
    """
    return value1 if condition else value2
