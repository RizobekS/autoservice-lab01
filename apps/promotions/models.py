from autoslug import AutoSlugField
from django.contrib.admin import display
from django.db import models
from image_cropping import ImageRatioField

from apps.tags.models import Tag
from utils.helpers import format_price


class Promotion(models.Model):
    title = models.CharField('Название акции', max_length=500)
    url = AutoSlugField(verbose_name='URL акции', unique=True, populate_from='title', editable=True)

    tags = models.ManyToManyField(verbose_name='Тэги', to=Tag, blank=True)
    active = models.BooleanField('Активно', help_text='Снимите галочку с "Активно" вместо удаления. Неактивные акции не отображаются нигде, кроме админ панели', default=True)
    date = models.DateField("Дата")
    show_at_homepage = models.BooleanField('Отображать на главной', default=False)
    fixed_price = models.BooleanField('Фиксированная цена', help_text='Фикс. цена: "990₽", НЕ фикс. цена: "от 990₽"', default=False)
    price = models.FloatField('Цена за работу (₽)')

    short_description = models.CharField('Краткое описание (до 500 символов)', max_length=500)
    text = models.TextField('Контент')

    image = models.ImageField('Изображение акции', help_text='Возможность обрезки появится после сохранения', upload_to='promotions/')
    thumbnail = ImageRatioField(verbose_name='Обрезка изображения для страницы списка акций (800x360)', image_field='image', size='800x360')
    icon_thumbnail = ImageRatioField(verbose_name='Обрезка изображения для списка "Другие акции" (100x100)', image_field='image', size='100x100')

    def __str__(self):
        return self.title

    @display(description='Цена')
    def verbose_price(self):
        price = format_price(self.price, '₽')
        return f'{price}' if self.fixed_price else f'От {price}'

    @display(description='Тэги')
    def tag_string(self):
        return ', '.join(item.name for item in self.tags.all())

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
