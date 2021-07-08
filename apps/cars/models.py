from autoslug import AutoSlugField
from django.contrib.admin import display
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django_cleanup.signals import cleanup_pre_delete

from apps.cars.utils.car_filter_mixin import CarFilterUtilsMixin
from apps.cars.utils.managers import LastAccessedManager
from apps.cars.utils.thumbnails import delete_old_thumbnails
from apps.cars.utils.validators import validate_double_slash_url
from autoservice.settings.common import AUTH_USER_MODEL


class CarFilter(models.Model, CarFilterUtilsMixin):
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    vendor = models.ForeignKey(verbose_name='Производитель', to='Vendor', on_delete=models.CASCADE)
    model = models.ForeignKey(verbose_name='Модель', to='Model', on_delete=models.CASCADE, null=True, blank=True)
    year = models.ForeignKey(verbose_name='Год', to='Year', on_delete=models.CASCADE, null=True, blank=True)
    modification = models.ForeignKey(verbose_name='Модификация', to='Modification', on_delete=models.CASCADE, null=True, blank=True)

    last_used = models.DateTimeField('Время последнего использования', auto_now=True)

    objects = LastAccessedManager()

    def __str__(self):
        return f'Filter #{self.id} {f" - {self.user} : " if self.user else ":"} {self.modification}'

    def __repr__(self):
        return f'CarFilter(user="{self.user}", vendor="{self.vendor.name}", model="{self.model.name}", year="{self.year.year}", modification="{self.modification.name}")'

    def is_full(self) -> bool:
        return bool(self.vendor) and bool(self.model) and bool(self.year) and bool(self.modification)

    def ceo_context(self):
        return self.existing_attributes()[-1].ceo_context()

    class Meta:
        unique_together = ('user', 'vendor', 'model', 'year', 'modification')
        get_latest_by = 'last_used'
        ordering = ['-last_used']
        verbose_name = 'Сохранённый ММП'
        verbose_name_plural = 'Сохранённые ММП'


class Vendor(models.Model):
    name = models.CharField('Название', max_length=200)
    url = AutoSlugField(verbose_name='URL марки', validators=[validate_double_slash_url], help_text='Заполняется на основе поля "Название"', populate_from='name',
                        unique=True, editable=True)
    logo = models.ImageField('Логотип', help_text="Возможность обрезки появится после сохранения", upload_to='vendor_logos')
    active = models.BooleanField('Активно', help_text='Снимите галочку с "Активно" вместо удаления', default=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Vendor(name="{self.name}", logo="{self.logo}")'

    def url_args(self):
        return (self.url,)

    @display(description='Связанные модели')
    def related_cars(self):
        cars = self.model_set
        if self.model_set.count() > 4:
            return f'Модели ({self.model_set.count()})'
        else:
            return ', '.join([car.name for car in cars.all()])

    def ceo_context(self):
        return {'vendor': self.name}

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'


class Model(models.Model):
    name = models.CharField('Название модели', max_length=200)
    url = AutoSlugField(verbose_name='URL модели', validators=[validate_double_slash_url], help_text='Заполняется на основе поля "Название"', populate_from='name', editable=True)

    vendor = models.ForeignKey(verbose_name='Производитель', to='Vendor', on_delete=models.CASCADE)  # TODO: change to on_delete=models.RESTRICT after final release

    def __str__(self):
        return f'{self.vendor.name} - {self.name}'

    def __repr__(self):
        return f'Model(name="{self.name}", vendor="{self.vendor.name}")'

    def url_args(self):
        return self.vendor.url, self.url

    @display(description='Года выпуска')
    def detailed_info(self):
        years = self.year_set
        if years.count() > 6:
            return f'{years.count()} разных годов выпуска'
        else:
            return mark_safe(', '.join([f'{year.year} <span style="color: grey">({year.modification_set.count()})</span>' for year in years.all()]))

    def ceo_context(self):
        return {'vendor': self.vendor.name, 'model': self.name}

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'


class Year(models.Model):
    year = models.PositiveSmallIntegerField('Год выпуска')

    model = models.ForeignKey(verbose_name='Модель', to='Model', on_delete=models.CASCADE)

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

    class Meta:
        verbose_name = 'Год выпуска'
        verbose_name_plural = 'Года выпуска'


class Modification(models.Model):
    name = models.CharField('Название модификации', max_length=200)

    year = models.ForeignKey(verbose_name='Года выпуска', to='Year', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.year.model.vendor.name} - {self.year.model.name} - {self.year.name} - {self.name}'

    def __repr__(self):
        return f'Modification(name="{self.name}", year="{self.year.year}", model="{self.year.model.name}", vendor="{self.year.model.vendor.name}")'

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


""" Signals """


# TODO: Check whether old images deletion works properly in production
def old_delete(file, **kwargs):
    delete_old_thumbnails(file, True)


cleanup_pre_delete.connect(old_delete)
