from django import template

from apps.accounts.forms import AuthenticationForm

register = template.Library()


@register.inclusion_tag('modals/login.html')
def login_modal():
    form = AuthenticationForm()
    return {'login_form': form}
