from django.db import models

from apps.services.utils.help_text import ACTIVE_HELP_TEXT


class EmailReceiver(models.Model):
    name = models.CharField('Имя получателя', max_length=200, null=True, blank=True)
    email = models.EmailField('Эл. почта')
    foreign_key = models.ForeignKey(verbose_name='Относится к филиалу', to='Branch', on_delete=models.CASCADE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Эл. почта получателя'
        verbose_name_plural = 'Эл. почты получателей'


class Branch(models.Model):
    name = models.CharField('Название', max_length=120)
    active = models.BooleanField('Активно', help_text=ACTIVE_HELP_TEXT, default=True)
    address = models.CharField('Адрес', max_length=240)
    phone = models.CharField('Тел. номер', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'


class StaticInformation(models.Model):
    name = models.CharField('Название', max_length=200)
    add_to_context = models.BooleanField('Добавлять в контекст', default=True)
    key = models.CharField('Ключ', max_length=200)
    value = models.CharField('Значение', max_length=500, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статическая информация'
        verbose_name_plural = 'Статическая информация'


class CEOSetting(models.Model):
    title = models.CharField('Заголовок', help_text='Содержимое тега title. Так-же поддерживает переменные.', max_length=200, blank=True)
    page = models.CharField('Описание страницы', max_length=120)
    key = models.CharField('Ключ', max_length=50, unique=True)
    variables = models.TextField('Доступные переменные', null=True, blank=True)
    description = models.TextField('Meta description', blank=True)
    keywords = models.TextField('Meta keywords', blank=True)
    robots = models.TextField('Meta robots', blank=True)

    def __str__(self):
        return f'Мета-теги для {self.page}'

    class Meta:
        verbose_name = 'CEO настройка'
        verbose_name_plural = 'CEO настройки'
