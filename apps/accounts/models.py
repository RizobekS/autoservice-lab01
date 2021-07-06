from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


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

    def create_superuser(self, email, first_name, password1, **other_fields):
        user = self._create_user(email, first_name, password1, save=False, **other_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser):
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30, null=True, blank=True)
    middle_name = models.CharField('Отчество', max_length=30, null=True, blank=True)
    email = models.EmailField('Электронная почта', help_text='Используется для регистрации авторизации', max_length=100, unique=True)
    username = models.CharField('Юзернейм', help_text='Не используется. Заполняется информацией из поля email', max_length=100)

    is_admin = models.BooleanField('Права админа', default=False)
    is_active = models.BooleanField('Активен', help_text='Неактивные пользователи не смогут войти на сайт. Вместо удаления пользователя просто снимите этот флажок.', default=True)
    is_staff = models.BooleanField('Права персонала', default=False)
    is_superuser = models.BooleanField('Суперпользователь', default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name',)

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    def __repr__(self):
        return f'User(email={self.email}, first_name={self.get_short_name()})'

    def get_short_name(self):
        return self.first_name

    def get_full_name(self) -> str:
        return ' '.join(filter(None, (self.last_name, self.first_name, self.middle_name)))

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
