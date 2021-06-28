from django.contrib.auth.forms import UserCreationForm

from apps.accounts.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'username')
