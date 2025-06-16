import requests
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from autoservice.settings.common import SMARTCAPTCHA_CLIENT_KEY, SMARTCAPTCHA_SERVER_KEY


class SmartCaptchaWidget(forms.Widget):
    template_name = 'includes/smartcaptcha_widget.html'
    is_required = True

    def __init__(self, attrs=None):
        default_attrs = {'class': 'smart-captcha', 'data-sitekey': SMARTCAPTCHA_CLIENT_KEY}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['sitekey'] = SMARTCAPTCHA_CLIENT_KEY
        return context


class SmartCaptchaField(forms.Field):
    widget = SmartCaptchaWidget()

    def clean(self, value):
        token = self.form.data.get("smart-token")

        if not token:
            raise ValidationError("Капча не пройдена или токен не получен")

        if not SMARTCAPTCHA_SERVER_KEY:
            raise ValidationError("SmartCaptcha server key is not set")

        try:
            response = requests.post(
                url='https://smartcaptcha.yandexcloud.net/validate',
                data={
                    'secret': SMARTCAPTCHA_SERVER_KEY,
                    'token': token,
                    'ip': '',  # можно прокинуть позже
                },
                timeout=3
            )
            result = response.json()
        except Exception as e:
            raise ValidationError(f"Ошибка при валидации SmartCaptcha: {e}")

        if result.get('status') != 'ok':
            raise ValidationError('SmartCaptcha не прошла. Попробуйте ещё раз.')

        return token
