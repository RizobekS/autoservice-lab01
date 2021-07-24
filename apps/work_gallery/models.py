import traceback

from autoslug import AutoSlugField
from django.db import models
from image_cropping import ImageRatioField


def work_gallery_image_path(instance, filename):
    return f'work_gallery/{instance.work.url}/{filename}'


class Image(models.Model):
    alt = models.CharField('Описание фото', help_text='Используется внутри аттрибута alt=" "', max_length=128, null=True, blank=True)
    image = models.ImageField('Изображение', help_text='Возможность обрезки появится после сохранения', upload_to=work_gallery_image_path)
    iframe_url = models.CharField('Ссылка на <iframe>', help_text='Оставьте поле пустым, чтобы отображать только изображение', max_length=512, null=True, blank=True)
    work = models.ForeignKey(verbose_name='Работа', to='Work', on_delete=models.CASCADE)
    list_thumbnail = ImageRatioField(verbose_name='Обрезка изображения', help_text='Для списка всех работ', image_field='image', free_crop=True)
    page_thumbnail = ImageRatioField(verbose_name='Обрезка изображения (1170x780)', help_text='Для индивидуальной страницы работы', image_field='image', size='1170x780')

    def __str__(self):
        return self.image.name

    def max_size(self):
        ratio = min(600 / self.image.width, 1)  # Downscale if image is wider than 600, do nothing otherwise
        width, height = self.image.width * ratio, self.image.height * ratio
        return f'{int(width)}x{int(height)}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Category(models.Model):
    name = models.CharField('Название категории', max_length=500)
    url = AutoSlugField(verbose_name='URL категории', unique=True, populate_from='title', editable=True, max_length=120)
    active = models.BooleanField('Активно', help_text='Снимите галочку с "Активно" вместо удаления. Неактивные категории не отображаются нигде, кроме админ панели', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Work(models.Model):
    title = models.CharField('Название работы', max_length=256)
    url = AutoSlugField(verbose_name='URL работы', unique=True, populate_from='title', editable=True, max_length=120)
    active = models.BooleanField('Активно', help_text='Снимите галочку с "Активно" вместо удаления. Неактивные работы не отображаются нигде, кроме админ панели', default=True)
    text = models.TextField('Описание работы')
    categories = models.ManyToManyField(verbose_name='Категории работы', to=Category, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'
