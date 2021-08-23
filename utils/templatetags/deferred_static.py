from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def deferred_style(url: str, class_: str = None):
    static_url = static(url)
    class_ = f'class="{class_}"' if class_ else ''
    return mark_safe(f"""<link rel="preload" href="{static_url}" as="style" onload="this.onload=null;this.rel='stylesheet'" {class_}>
  <noscript>
    <link rel="stylesheet" href="{static_url}">
  </noscript>""")
