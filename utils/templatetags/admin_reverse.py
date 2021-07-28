from django import template
from django.db.models import Model
from django.http import HttpRequest
from django.urls import reverse

from utils.helpers import link_tag_safe

register = template.Library()


@register.simple_tag
def admin_reverse(instance: Model, link_name: str = None, request: HttpRequest = None):
    """
        Returns html link to admin change page of an item

        instance - required. Subclass of models.Model. It is used to retrieve model_name, app_label and PK field to construct url
        link_name - optional. If provided - used inside <a> tag. If not provided - __str__ of instance is used instead
        request - optional. If provided - url is made absolute (with protocol and host)
    """

    if not isinstance(instance, Model):
        raise ValueError('Instance must inherit from models.Model')

    url = reverse("admin:%s_%s_change" % (instance._meta.model._meta.app_label, instance._meta.model_name), args=(instance.pk,))
    url = request.build_absolute_uri(url)
    return link_tag_safe(url, link_name if link_name else str(instance), target_blank=True)
