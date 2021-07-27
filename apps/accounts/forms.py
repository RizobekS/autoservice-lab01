from django import forms
from django.conf import settings
from django.contrib.auth.forms import \
    UserCreationForm as BaseUserCreationForm, \
    AuthenticationForm as BaseAuthenticationForm, \
    PasswordChangeForm as BasePasswordChangeForm, UsernameField, \
    PasswordResetForm as BasePasswordResetForm, SetPasswordForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from apps.accounts.models import User, Appointment, ShortAppointment
from apps.site_settings.models import StaticInformation
from utils.shortcuts import add_attrs


class RegistrationForm(BaseUserCreationForm):
    CLASSES = 'form-control text-center woocommerce-Input woocommerce-Input--text input-text'

    password1 = forms.CharField(label='Пароль', strip=False,
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': CLASSES + ' divider-20', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Подтверждение пароля', strip=False,
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': CLASSES, 'placeholder': 'Повторите пароль'}))

    class Meta:
        CLASSES = 'form-control text-center woocommerce-Input woocommerce-Input--text input-text'

        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'password1', 'password2')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': CLASSES, 'placeholder': 'Имя', 'autofocus': True}),
            'last_name': forms.TextInput(attrs={'class': CLASSES, 'placeholder': 'Фамилия'}),
            'middle_name': forms.TextInput(attrs={'class': CLASSES, 'placeholder': 'Отчество'}),
            'email': forms.EmailInput(attrs={'class': CLASSES + ' divider-20', 'placeholder': 'Электронная почта'}),
        }

        error_messages = {
            'email': {
                'unique': 'Пользователь с таким адресом эл. почты уже существует.'
            }
        }


class AuthenticationForm(BaseAuthenticationForm):
    error_messages = {
        'invalid_login': 'Пожалуйста введите верный адрес эл. почты и/или пароль.',
        'inactive': _("This account is inactive."),
    }
    username = UsernameField(widget=forms.EmailInput(attrs={'autofocus': True, 'placeholder': 'Электронная почта', 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False,
                               widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'placeholder': 'Пароль', 'class': 'form-control'}))


class PasswordResetForm(BasePasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        PLACEHOLDERS = {'email': 'Эл. почта'}
        CLASSES = 'form-control woocommerce-Input woocommerce-Input--text input-text'
        add_attrs(self, placeholders=PLACEHOLDERS, classes=CLASSES)


class NewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        PLACEHOLDERS = {'new_password1': 'Новый пароль', 'new_password2': 'Подтверждение пароля'}
        CLASSES = 'form-control woocommerce-Input woocommerce-Input--text input-text'
        add_attrs(self, placeholders=PLACEHOLDERS, classes=CLASSES)


class ProfileEditForm(forms.ModelForm):
    ACTION_NAME = 'profile'
    action = forms.CharField(widget=forms.HiddenInput(attrs={'value': ACTION_NAME}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        PLACEHOLDERS = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'email': 'Email',
        }
        CLASSES = 'form-control woocommerce-Input woocommerce-Input--text input-text'
        add_attrs(self, placeholders=PLACEHOLDERS, classes=CLASSES)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'email')


class PasswordChangeForm(BasePasswordChangeForm):
    ACTION_NAME = 'password'
    action = forms.CharField(widget=forms.HiddenInput(attrs={'value': ACTION_NAME}))

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        PLACEHOLDERS = {
            'old_password': 'Старый пароль',
            'new_password1': 'Новый пароль',
            'new_password2': 'Повторите новый пароль'
        }
        CLASSES = 'form-control woocommerce-Input woocommerce-Input--password input-text'
        add_attrs(self, placeholders=PLACEHOLDERS, classes=CLASSES)


class AppointmentForm(forms.ModelForm):
    email_subject_template = 'accounts/emails/appointment/subject.html'
    email_body_template = 'accounts/emails/appointment/body.html'
    extra_context = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].empty_label = 'Выберите СТО'

    def send_mail(self):
        if not self.is_valid():
            raise ValueError('The form must be valid to send mails')
        branch = self.cleaned_data.get('branch')
        site_name = StaticInformation.objects.get(key='site_name')
        context = {'site_name': site_name.value, **self.cleaned_data, **self.extra_context}
        send_mail(
            render_to_string(self.email_subject_template, context=context),
            render_to_string(self.email_body_template, context=context),
            settings.DEFAULT_FROM_EMAIL,
            branch.get_email_list(),
            fail_silently=True
        )

    class Meta:
        fields = ('user', 'full_name', 'car', 'phone', 'branch', 'datetime')
        model = Appointment


class ShortAppointmentForm(AppointmentForm):
    email_subject_template = 'accounts/emails/short_appointment/subject.html'
    email_body_template = 'accounts/emails/short_appointment/body.html'

    def send_mail(self):
        self.extra_context = {'datetime': self.instance.datetime}
        return super().send_mail()

    class Meta:
        fields = ('full_name', 'phone', 'email', 'branch', 'text')
        model = ShortAppointment
