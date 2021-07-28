from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.site_settings.models import StaticInformation


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=256, required=True)
    email = forms.EmailField(label='Email', required=True)
    text = forms.CharField(label='Сообщение', widget=forms.Textarea, required=True)

    def send_mail(self, request):
        if not self.is_valid():
            raise ValueError('The form must be valid to send mails')

        site_name = StaticInformation.objects.get(key='site_name')
        receiver = StaticInformation.objects.get(key='email')
        return send_mail(
            render_to_string('contacts/emails/subject.txt', context={'site_name': site_name.value}),
            render_to_string('contacts/emails/body.txt', context={'site_name': site_name.value, **self.cleaned_data}),
            settings.DEFAULT_FROM_EMAIL,
            [receiver.value],
            fail_silently=True
        )
