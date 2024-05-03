from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts.utils.managers import UserManager
from autoservice.settings.common import AUTH_USER_MODEL


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


class Appointment(models.Model):
    CHOICES = (('pending', 'Ожидает подтверждения'),
               ('confirmed', 'Подтверждена'),
               ('completed', 'Услуга оказана'))

    user = models.ForeignKey(verbose_name='Пользователь', to=AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    full_name = models.CharField('Полное имя', max_length=200)
    car = models.CharField('Автомобиль', max_length=400)
    phone = models.CharField('Телефон', max_length=26)
    branch = models.ForeignKey(verbose_name='Филиал', to='site_settings.Branch', on_delete=models.RESTRICT)
    datetime = models.DateTimeField('Дата и время, указанные пользователем', null=True)
    created_date = models.DateTimeField('Дата и время создания заявки', auto_now_add=True, null=True, blank=True)

    status = models.CharField('Статус', max_length=20, choices=CHOICES, default='pending')

    def __str__(self):
        return f'Заявка от {self.full_name}' + (f', {self.datetime.strftime("%m/%d/%Y, %H:%M")}' if self.datetime is not None else '')

    class Meta:
        ordering = ['-datetime']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class ShortAppointment(models.Model):
    full_name = models.CharField('Полное имя', max_length=256)
    phone = models.CharField('Телефон', max_length=26)
    email = models.EmailField('Эл. почта', null=True, blank=True)
    branch = models.ForeignKey(verbose_name='Филиал', to='site_settings.Branch', on_delete=models.RESTRICT)
    text = models.TextField('Сообщение', null=True, blank=True)
    datetime = models.DateTimeField('Дата и время создания заявки', auto_now_add=True)

    def __str__(self):
        return f'Мини-заявка от {self.full_name} ({self.datetime.strftime("%m/%d/%Y, %H:%M")})' if self.datetime else f'Мини-заявка от {self.full_name}'

    class Meta:
        verbose_name = 'Мини-заявка'
        verbose_name_plural = 'Мини-заявки'


class SparePartAppointment(models.Model):
    full_name = models.CharField('Полное имя', max_length=256)
    phone = models.CharField('Телефон', max_length=26)
    car = models.CharField('Автомобиль', max_length=400, null=True, blank=True)
    branch = models.ForeignKey(verbose_name='Филиал', to='site_settings.Branch', on_delete=models.RESTRICT)
    vin = models.CharField('VIN номер', max_length=17, null=True, blank=True)
    text = models.TextField('Сообщение', null=True, blank=True)
    datetime = models.DateTimeField('Дата и время создания заявки', auto_now_add=True)

    def __str__(self):
        return f'Заявка на запчасти от {self.full_name} ({self.datetime.strftime("%m/%d/%Y, %H:%M")})' if self.datetime else f'Заявка на запчасти от {self.full_name}'

    class Meta:
        verbose_name = 'Заявка на запчасти'
        verbose_name_plural = 'Заявки на запчасти'


class CallRequest(models.Model):
    phone = models.CharField('Телефон', max_length=26)
    branch = models.ForeignKey(verbose_name='Филиал', to='site_settings.Branch', on_delete=models.RESTRICT)
    datetime = models.DateTimeField('Дата и время создания заявки', auto_now_add=True)

    def __str__(self):
        return f'Заказ на звонок: {self.phone} ({self.datetime.strftime("%m/%d/%Y, %H:%M")})' if self.datetime else f'Заказ на звонок: {self.phone}'

    class Meta:
        verbose_name = 'Заказ на звонок'
        verbose_name_plural = 'Заказы на звонок'


class BodyRepairAppointment(models.Model):
    car = models.CharField('Автомобиль', max_length=400, null=True, blank=True)
    description = models.TextField('Описание')
    branch = models.ForeignKey(verbose_name='Филиал', to='site_settings.Branch', on_delete=models.RESTRICT)
    full_name = models.CharField('Полное имя', max_length=256)
    phone = models.CharField('Телефон', max_length=26)
    datetime = models.DateTimeField('Дата и время создания заявки', auto_now_add=True)

    def __str__(self):
        return f'Заявка на оценку кузовного ремонта от {self.full_name} ({self.datetime.strftime("%m/%d/%Y, %H:%M")})' \
            if self.datetime else f'Заявка на оценку кузовного ремонта от {self.full_name}'

    class Meta:
        verbose_name = 'Заявка на оценку кузовного ремонта'
        verbose_name_plural = 'Заявки на оценку кузовного ремонта'


class BodyRepairAppointmentImage(models.Model):
    appointment = models.ForeignKey(verbose_name='Заявка на кузовной ремонт', to='accounts.BodyRepairAppointment',
                                    on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Изображение', upload_to='body_repair_appointments/')

    def __str__(self):
        return f'Изображение с "{self.appointment}"'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
