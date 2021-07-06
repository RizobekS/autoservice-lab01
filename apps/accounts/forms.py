from django import forms
from django.contrib.auth.forms import \
    UserCreationForm as BaseUserCreationForm, \
    AuthenticationForm as BaseAuthenticationForm, \
    PasswordChangeForm as BasePasswordChangeForm, UsernameField, \
    PasswordResetForm as BasePasswordResetForm, SetPasswordForm
from django.utils.translation import gettext as _

from apps.accounts.models import User
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
