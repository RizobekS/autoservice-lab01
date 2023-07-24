from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def get_promotion_url(promotion: "Promotion"):
    if promotion.absolute_url:
        return promotion.absolute_url

    return reverse('promotions:promotion', args=(promotion.url,))
