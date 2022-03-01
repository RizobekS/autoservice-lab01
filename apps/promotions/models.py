from autoslug import AutoSlugField
from django.contrib.admin import display
from django.db import models
from django.urls import reverse
from image_cropping import ImageRatioField

from apps.tags.models import Tag
from utils.helpers import format_price


class Category(models.Model):
    CEO_HELP_TEXT = 'Оставьте поле пустым чтобы использовать стандартную маску.'
    name = models.CharField('Название категории', max_length=500)
    url = AutoSlugField(verbose_name='URL категории', unique=True, populate_from='title', editable=True, max_length=120)

    meta_title = models.CharField('Заголовок <title>', help_text=CEO_HELP_TEXT, max_length=200, blank=True)
    meta_header = models.CharField('Заголовок <h1>', help_text=CEO_HELP_TEXT, max_length=200, blank=True)
    meta_description = models.TextField('Meta description', help_text=CEO_HELP_TEXT, null=True, blank=True)
    meta_keywords = models.TextField('Meta keywords', help_text=CEO_HELP_TEXT, null=True, blank=True)
    meta_robots = models.TextField('Meta robots', help_text=CEO_HELP_TEXT, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('promotions:category', args=(self.url,))

    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Promotion(models.Model):
    CEO_HELP_TEXT = 'Оставьте поле пустым чтобы использовать маску категории или стандартную маску.'
    IS_SALE_CHOICES = (
        (True, 'Скидка'),
        (False, 'Цена')
    )

    title = models.CharField('Название акции', max_length=500)
    url = AutoSlugField(verbose_name='URL акции', unique=True, populate_from='title', editable=True, max_length=120)

    tags = models.ManyToManyField(verbose_name='Тэги', to=Tag, blank=True)
    category = models.ForeignKey(verbose_name='Категория (Тип)', to=Category, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField('Активно', help_text='Снимите галочку с "Активно" вместо удаления. Неактивные акции не отображаются нигде, кроме админ панели', default=True)
    date = models.DateField('Дата')
    short_description = models.CharField('Краткое описание (до 500 символов)', max_length=500)
    text = models.TextField('Контент')

    fixed_price = models.BooleanField('Фиксированная цена/скидка', help_text='Фикс. цена: "990₽", НЕ фикс. цена: "от 990₽". Фикс. скидка: "15%", НЕ фикс. скидка: "До 15%"',
                                      default=False)
    price = models.FloatField('Цена (₽) / Скидка (%)', null=True, blank=True)
    sale = models.BooleanField('Цена/Скидка', default=False, choices=IS_SALE_CHOICES)

    show_at_homepage = models.BooleanField('Отображать на главной', default=False)
    homepage_description = models.CharField('Краткое описание для главной страницы (до 500 символов)', max_length=500, blank=True)

    image = models.ImageField('Изображение акции', help_text='Возможность обрезки появится после сохранения', upload_to='promotions/', max_length=256)
    thumbnail = ImageRatioField(verbose_name='Обрезка изображения для страницы списка акций (800x360)', image_field='image', size='800x360')
    icon_thumbnail = ImageRatioField(verbose_name='Обрезка изображения для списка "Другие акции" (100x100)', image_field='image', size='100x100')

    articles = models.ManyToManyField(verbose_name='Привязанные статьи', to='news.Article', blank=True)
    products = models.ManyToManyField(verbose_name='Привязанные услуги', to='services.Product', blank=True)

    meta_title = models.CharField('Заголовок <title>', help_text=CEO_HELP_TEXT, max_length=200, blank=True)
    meta_header = models.CharField('Заголовок <h1>', help_text=CEO_HELP_TEXT, max_length=200, blank=True)
    meta_description = models.TextField('Meta description', help_text=CEO_HELP_TEXT, null=True, blank=True)
    meta_keywords = models.TextField('Meta keywords', help_text=CEO_HELP_TEXT, null=True, blank=True)
    meta_robots = models.TextField('Meta robots', help_text=CEO_HELP_TEXT, null=True, blank=True)

    def __str__(self):
        return self.title

    @display(description='Цена/Скидка')
    def verbose_price(self):
        if self.price:
            price = format_price(self.price, self.get_currency())
            return f'{price}' if self.fixed_price else f'От {price}'
        else:
            return '-'

    def get_currency(self):
        return '%' if self.sale else '₽'

    @display(description='Тэги')
    def tag_string(self):
        return ', '.join(item.name for item in self.tags.all())

    def reverse_url(self):
        return reverse('promotions:promotion', args=(self.url,))

    def get_absolute_url(self):
        return reverse('promotions:promotion', args=(self.url,))

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
