from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, raw_password, save=False, last_name=None, middle_name=None, **other_fields):
        if not first_name:
            raise ValueError('Имя не указано')
        if not email:
            raise ValueError('Эл. почта не указана')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, email=email, username=email, last_name=last_name, middle_name=middle_name)
        user.set_password(raw_password)
        if save:
            user.save()
        return user

    def create_user(self, email, first_name, password1, **other_fields):
        return self._create_user(email, first_name, password1, save=True, **other_fields)

    def create_superuser(self, email, first_name, password, **other_fields):
        user = self._create_user(email, first_name, password, save=False, **other_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
