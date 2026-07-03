from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.contacts.models import ContactMessage
from apps.site_settings.models import StaticInformation
from utils.calltouch import send_calltouch_request


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'text')

    def send_mail(self, request):
        if not self.is_valid():
            raise ValueError('The form must be valid to send mails')

        site_name = StaticInformation.objects.get(key='site_name')
        receiver = StaticInformation.objects.get(key='email')
        context = {'site_name': site_name.value, **self.cleaned_data}
        return send_mail(
            render_to_string('contacts/emails/subject.txt', context=context),
            render_to_string('contacts/emails/body.txt', context=context),
            settings.DEFAULT_FROM_EMAIL,
            [receiver.value],
            fail_silently=True,
            html_message=render_to_string('contacts/emails/html.html', context, request=request)
        )

    def send_calltouch_request(self, request):
        send_calltouch_request(
            request=request,
            subject='Сообщение из раздела "Контакты"',
            full_name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            text=self.cleaned_data['text'],
        )
