from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def is_active(context: dict, *namespaces: str, class_: str = 'active'):
    """
        Returns 'active' (can be changed) if request.resolver.namespace is in passed list of strings and "" otherwise

        namespaces: List[str] - namespaces to compare to (Either single or multiple str values)
        class_: str - string to return if namespace matches current one. 'active' by default
    """
    request = context.get('request')
    if request is None:
        raise ValueError('Usage of is_active template tag requires request in context')

    for ns in namespaces:
        if request.resolver_match.view_name.startswith(ns):
            return class_
    return ''


@register.simple_tag(takes_context=True)
def is_active_path(context: dict, url: str, class_: str = 'active'):
    """
        Returns class="active" if request.path_info is equal to passed string and "" otherwise

        url: str - namespaces to compare to (Either single or multiple str values)
    """
    request = context.get('request')
    if request is None:
        raise ValueError('Usage of is_active_path template tag requires request in context')

    return class_ if url == request.path_info else ''
