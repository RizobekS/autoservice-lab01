from django import template

from apps.accounts.forms import AppointmentForm
from utils.car_filter import get_car_filter

register = template.Library()


@register.inclusion_tag('modals/online-appointment.html', takes_context=True)
def appointment_modal(context):
    request = context.get('request')
    if request is None:
        raise ValueError('Usage of appointment_modal template tag requires request in context')

    if request.user.is_authenticated:
        car = request.user.carfilter_set.latest()
    else:
        car = get_car_filter(request)

    initial = {
        'full_name': request.user.get_full_name() if request.user.is_authenticated else '',
        'car': car.full_name() if car else '',
    }

    form = AppointmentForm(initial=initial)
    return {'appointment_form': form}
