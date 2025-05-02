from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from image_cropping import ImageRatioField

from apps.cars.utils.car_filter_mixin import CarFilterUtilsMixin
from apps.cars.utils.validators import validate_double_slash_url
from autoservice.settings.common import AUTH_USER_MODEL


class CarFilter(models.Model, CarFilterUtilsMixin):
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    vendor = models.ForeignKey(verbose_name='Производитель', to='Vendor', on_delete=models.CASCADE)
    model = models.ForeignKey(verbose_name='Модель', to='Model', on_delete=models.CASCADE, null=True, blank=True)
    year = models.ForeignKey(verbose_name='Год', to='Year', on_delete=models.CASCADE, null=True, blank=True)
    modification = models.ForeignKey(verbose_name='Модификация', to='Modification', on_delete=models.CASCADE, null=True, blank=True)

    last_used = models.DateTimeField('Время последнего использования', auto_now=True)

    def __str__(self):
        return f'Filter #{self.id} {f" - {self.user} : " if self.user else ":"} {self.modification}'

    def __repr__(self):
        return f'CarFilter(user="{self.user}", vendor="{self.vendor.name}", model="{self.model.name}")'

    def is_full(self) -> bool:
        return bool(self.vendor) and bool(self.model)

    def ceo_context(self):
        return self.existing_attributes()[-1].ceo_context()

    def update_last_used(self):
        # print(traceback.print_stack())
        if self.user and CarFilter.objects.latest().id != self.id:
            self.last_used = timezone.now()
            self.save(update_fields=('last_used',))

    class Meta:
        indexes = (models.Index(fields=('last_used',)),
                   models.Index(fields=('user_id',)))
        unique_together = ('user', 'vendor', 'model', 'year', 'modification')
        get_latest_by = 'last_used'
        ordering = ['-last_used']
        verbose_name = 'Сохранённый ММП'
        verbose_name_plural = 'Сохранённые ММП'


class Vendor(models.Model):
    name = models.CharField('Название', max_length=200)
    url = AutoSlugField(verbose_name='URL марки', validators=[validate_double_slash_url], help_text='Заполняется на основе поля "Название"', populate_from='name',
                        unique=True, editable=True, max_length=120)
    header_image = models.ImageField('Изображение в заголовке', help_text='Возможность обрезки появится после сохранения', null=True, blank=True)
    header_crop = ImageRatioField(verbose_name='Обрезка изображения заголовка (1920x600)', image_field='header_image', size='1920x600')
    logo = models.ImageField('Логотип', help_text='Возможность обрезки появится после сохранения', upload_to='vendor_logos', max_length=256)
    favicon = models.ImageField('Значок страницы (favicon)', upload_to='vendor_favicons', max_length=256, null=True, blank=True,
                                help_text='Значок будет отображаться при данной марке в ММП фильтре. Оставьте поле пустым чтобы использовать стандартный значок.')
    active = models.BooleanField('Активно', help_text='Снимите галочку с "Активно" вместо удаления', default=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Vendor(name="{self.name}", logo="{self.logo}")'

    def url_args(self):
        return (self.url,)

    def ceo_context(self):
        return {'vendor': self.name}

    def active_model_set(self):
        return self.model_set.filter(active=True)

    class Meta:
        ordering = ('name',)
        indexes = (models.Index(fields=('active',)),)
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'


class Model(models.Model):
    name = models.CharField('Название модели', max_length=200)
    url = AutoSlugField(verbose_name='URL модели', validators=[validate_double_slash_url], help_text='Заполняется на основе поля "Название"', populate_from='name', editable=True,
                        max_length=120)
    active = models.BooleanField('Активно', help_text='Снимите галочку с "Активно" вместо удаления', default=True)
    header_image = models.ImageField('Изображение в заголовке', upload_to='model_header_images', null=True, blank=True,
                                     help_text='Возможность обрезки появится после сохранения. Оставьте пустым, чтобы использовать изображение марки.')
    header_crop = ImageRatioField(verbose_name='Обрезка изображения заголовка (1920x600)', image_field='header_image', size='1920x600')

    vendor = models.ForeignKey(verbose_name='Производитель', to='Vendor', on_delete=models.CASCADE)  # TODO: change to on_delete=models.RESTRICT after final release

    def __str__(self):
        return f'{self.vendor.name} - {self.name}'

    def __repr__(self):
        return f'Model(name="{self.name}", vendor="{self.vendor.name}")'

    def url_args(self):
        return self.vendor.url, self.url

    def ceo_context(self):
        return {'vendor': self.vendor.name, 'model': self.name}

    def active_year_set(self):
        return self.year_set.filter(active=True)

    class Meta:
        ordering = ('vendor',)
        indexes = (models.Index(fields=('active',)),)
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'


class Year(models.Model):
    year = models.PositiveSmallIntegerField('Год выпуска')

    model = models.ForeignKey(verbose_name='Модель', to='Model', on_delete=models.CASCADE)
    active = models.BooleanField('Активно', help_text='Снимите галочку с "Активно" вместо удаления', default=True)

    def __str__(self):
        return f'{self.model.vendor.name} - {self.model.name} - {self.year}'

    def __repr__(self):
        return f'Year(year="{self.year}", model="{self.model.name}", vendor="{self.model.vendor.name}")'

    def url_args(self):
        return self.model.vendor.url, self.model.url, self.url

    # An alias for compatibility with other filter parts
    @property
    def url(self):
        return str(self.year)

    # An alias for compatibility with other filter parts
    @property
    def name(self):
        return str(self.year)

    def ceo_context(self):
        return {'vendor': self.model.vendor.name, 'model': self.model.name, 'year': self.name}

    def active_modification_set(self):
        return self.modification_set.filter(active=True)

    class Meta:
        indexes = (models.Index(fields=('year',)),)
        verbose_name = 'Год выпуска'
        verbose_name_plural = 'Года выпуска'


class Modification(models.Model):
    name = models.CharField('Название модификации', max_length=200)
    full_name = models.CharField('Полное название автомобиля', max_length=640, null=True, blank=True)
    year = models.ForeignKey(verbose_name='Года выпуска', to='Year', on_delete=models.CASCADE)
    active = models.BooleanField('Активно', help_text='Снимите галочку с "Активно" вместо удаления', default=True)

    def __str__(self):
        if not self.full_name:
            self.save(update_fields=('full_name',))
        return self.full_name

    def __repr__(self):
        return f'Modification(name="{self.name}", year="{self.year.year}", model="{self.year.model.name}", vendor="{self.year.model.vendor.name}")'

    def save(self, **kwargs):
        self.full_name = f'{self.year.model.vendor.name} - {self.year.model.name} - {self.year.name} - {self.name}'
        return super().save(**kwargs)

    def url_args(self):
        return self.year.model.vendor.url, self.year.model.url, self.year.url, self.url

    # An alias for compatibility with other filter parts
    @property
    def url(self):
        return str(self.id)

    def ceo_context(self):
        return {'vendor': self.year.model.vendor.name, 'model': self.year.model.name, 'year': self.year.name, 'modification': self.name}

    class Meta:
        verbose_name = 'Модификация'
        verbose_name_plural = 'Модификации'
