from typing import Dict, Any

from django.contrib import messages
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin, ProcessFormView

from apps.accounts.forms import ShortAppointmentForm, SparePartAppointmentForm
from utils.breadcrumbs.mixins import BreadcrumbsMixin
from utils.breadcrumbs.types import Breadcrumb


class PersonalAreaMixin(BreadcrumbsMixin, ContextMixin):
    """
        Adds necessary context for Personal area, helps building breadcrumbs
    """
    initial_breadcrumbs = [Breadcrumb('Личный кабинет', reverse_lazy('accounts:pa:index'))]

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        extra_context = {
            'page_title': 'Личный кабинет',
            'image_url': static('images/lk/lk-header.jpg'),
            'image_alt': 'Retro car',
        }
        context.update(extra_context)
        return context


class ShortAppointmentMixin(FormMixin, ProcessFormView):
    """
        Adds functionality to render and process ShortAppointmentForm
    """
    form_class = ShortAppointmentForm

    def form_valid(self, form):
        form.save()
        form.send_mail(self.request)
        form.send_calltouch_request(self.request)
        messages.success(self.request, 'Заявка была успешно отправлена ✔', extra_tags='text-success')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path_info


class SparePartAppointmentMixin(FormMixin, ProcessFormView):
    """
        Adds functionality to render and process SparePartAppointment
    """
    form_class = SparePartAppointmentForm

    def form_valid(self, form):
        obj = form.save()
        form.send_mail(self.request)
        form.send_calltouch_request(self.request)
        messages.success(self.request, 'Заявка была успешно отправлена ✔', extra_tags='text-success')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path_info
