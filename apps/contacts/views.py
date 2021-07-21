from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.contacts.forms import ContactForm
from utils.mixins import PageSettingsMixin


class ContactsView(FormView, PageSettingsMixin):
    template_name = 'contacts/contacts.html'
    viewname = 'contacts:contacts'

    form_class = ContactForm
    success_url = reverse_lazy('contacts:contacts')

    def form_valid(self, form):
        if form.send_mail():
            messages.success(self.request, '✔ Сообщение было отправлено', extra_tags='text-success')
        else:
            messages.error(self.request, '❌ Сообщение не было отправлено. Что-то пошло не так...', extra_tags='text-danger')
        return super().form_valid(form)
