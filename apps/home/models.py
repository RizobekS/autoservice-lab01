from adminsortable.models import SortableMixin
from django.db import models
from image_cropping import ImageRatioField


class Slide(SortableMixin):
    static_text = models.CharField('Подзаголовок', max_length=200)
    animated_text = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание', max_length=900, null=True, blank=True)
    active = models.BooleanField('Активно', help_text='Снимите галочку с "Активно" вместо удаления', default=True)
    button_text = models.CharField('Текст кнопки', max_length=100)
    link = models.CharField('Ссылка', max_length=200, null=True, blank=True)
    background_image = models.ImageField('Картинка', upload_to='slides', null=True, blank=True)
    sorting = models.PositiveIntegerField('Сортировка', editable=False)

    def __str__(self):
        return self.static_text + ' ' + self.animated_text

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'
        ordering = ['sorting']
