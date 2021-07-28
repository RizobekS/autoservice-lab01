from django.contrib.admin import display
from django.db import models
from image_cropping import ImageRatioField


class Position(models.Model):
    name = models.CharField('Название должности', max_length=50, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Position(name={self.name})'

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Master(models.Model):
    name = models.CharField('Имя мастера', max_length=100)
    show_at_homepage = models.BooleanField('Отображать на Главной странице', default=False)
    active = models.BooleanField('Активно', help_text='Снимите галочку с "Активно" вместо удаления. Неактивные мастера не отображаются нигде, кроме админ панели', default=True)
    positions = models.ManyToManyField(verbose_name='Должность', to=Position, blank=True)
    credo = models.TextField('Кредо')
    image = models.ImageField('Фото', help_text='Возможность обрезки появится после сохранения', upload_to='masters', max_length=256)
    thumbnail = ImageRatioField(verbose_name='Обрезка изображения (350x350)', image_field='image', size='350x350')

    def __str__(self):
        position_string = self.position_string()
        return f'{self.name} - {position_string}' if position_string else self.name

    def __repr__(self):
        return f'Master(name={self.name}, positions={self.position_string()})'

    @display(description='Должности', empty_value='-')
    def position_string(self):
        return ', '.join(item.name for item in self.positions.all())

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'
