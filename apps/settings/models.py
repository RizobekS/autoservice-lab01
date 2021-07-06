from django.contrib.admin import display
from django.db import models

from apps.services.utils.help_text import ACTIVE_HELP_TEXT


# class Page(models.Model):
#     name = models.CharField('Имя страницы (из urls.py)', max_length=200, unique=True)
#     template_name = models.CharField('Путь к шаблону', max_length=200, null=True, blank=True)
#     parent_page = models.ForeignKey(verbose_name='Следует после (в хлебных крошках)', to='Page', on_delete=models.DO_NOTHING, null=True, blank=True)
#     sorting = models.PositiveIntegerField('Порядок отображения в меню', default=0, blank=False, null=False)
#     title = models.CharField('Заголовок страницы', max_length=200)
#     show_in_menu = models.BooleanField('Показывать в меню', default=False)
#     menu_name = models.CharField('Название в меню', help_text='Оставьте пустым, чтобы использовать заголовок страницы', max_length=200, null=True, blank=True)
#     meta_description = models.CharField('Описание (мета-тег)', help_text='Необязательно. Используется для SEO.', max_length=1000, null=True, blank=True)
#     meta_keywords = models.CharField('Ключевые слова (мета-тег)', help_text='Необязательно. Используется для SEO.', max_length=500, null=True, blank=True)
#     meta_robots = models.CharField('Robots (мета-тег)', help_text='Необязательно. Используется для SEO.', max_length=500, null=True, blank=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         ordering = ['sorting']
#         verbose_name = 'Настройки страницы'
#         verbose_name_plural = 'Настройки страниц'


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

    @display(description='Получатели эл. сообщений')
    def receivers_string(self):
        return f'({self.emailreceiver_set.count()}) {" ,  ".join(item.email for item in self.emailreceiver_set.all())}'

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'


class StaticInformation(models.Model):
    name = models.CharField('Название', max_length=200)
    add_to_context = models.BooleanField('Добавлять в контекст', default=True)
    key = models.CharField('Ключ', max_length=200)
    value = models.CharField('Значение', max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статическая информация'
        verbose_name_plural = 'Статическая информация'
