from adminsortable.models import SortableMixin
from autoslug import AutoSlugField
from django.contrib.admin import display
from django.db import models
from django.urls import reverse
from image_cropping import ImageRatioField

from apps.cars.utils.validators import validate_double_slash_url
from apps.services.utils.fields import OptimizedManyToManyField
from apps.services.utils.help_text import DESCRIPTION_HELP_TEXT, TITLE_DATIVE_HELP_TEXT, ACTIVE_HELP_TEXT, VENDOR_PAGE_THUMBNAIL_HELP_TEXT, SUPPORTS_CAR_CONTEXT_HELP_TEXT
from apps.tags.models import Tag
from utils.helpers import format_price


class Section(SortableMixin):
    CEO_HELP_TEXT = 'Оставьте поле пустым чтобы использовать стандартную маску.'

    title = models.CharField('Название раздела', max_length=255)
    url = AutoSlugField(verbose_name='URL раздела', help_text='Заполняется на основе поля "Название раздела"',
                        validators=[validate_double_slash_url], populate_from='title', unique=True, editable=True, max_length=120)
    title_dative = models.CharField('Название раздела в Дательном падеже', help_text=TITLE_DATIVE_HELP_TEXT, max_length=255)
    active = models.BooleanField('Активно', help_text=ACTIVE_HELP_TEXT, default=True)
    show_at_homepage = models.BooleanField('Отображать на главной', help_text='В блоке "Наши услуги"', default=False)
    short_description = models.CharField('Краткое описание', max_length=255)
    description = models.TextField('Содержание', help_text=' '.join((DESCRIPTION_HELP_TEXT, SUPPORTS_CAR_CONTEXT_HELP_TEXT)), blank=True, null=True)
    parent_section = models.ForeignKey(verbose_name='Родительский раздел', to='Section', help_text='Оставьте поле пустым, если данный раздел - корневой',
                                       on_delete=models.SET_NULL, null=True, blank=True)

    image = models.ImageField('Изображение', help_text='Возможность обрезки появится после сохранения', upload_to='services/sections', max_length=256)
    thumbnail_1960x600 = ImageRatioField(verbose_name='Обрезка изображения (1920x600)', help_text='Для фона заголовка страницы', image_field='image', size='1920x600')
    thumbnail_960x585 = ImageRatioField(verbose_name='Обрезка изображения (960x585)', help_text=VENDOR_PAGE_THUMBNAIL_HELP_TEXT, image_field='image', size='960x585')
    thumbnail_455x200 = ImageRatioField(verbose_name='Обрезка изображения (455x200)', help_text='Для превью на странице раздела 1 уровня', image_field='image', size='455x200')
    thumbnail_348x236 = ImageRatioField(verbose_name='Обрезка изображения (348x236)', image_field='image', size='348x236')
    thumbnail_268x118 = ImageRatioField(verbose_name='Обрезка изображения (268x118)', image_field='image', size='268x118')
    thumbnail_80x80 = ImageRatioField(verbose_name='Обрезка изображения (80x80)', image_field='image', size='80x80')

    meta_title = models.CharField('Заголовок <title>', help_text=CEO_HELP_TEXT, max_length=200, blank=True)
    meta_header = models.CharField('Заголовок <h1>', help_text=CEO_HELP_TEXT, max_length=200, blank=True)
    meta_description = models.TextField('Meta description', help_text=CEO_HELP_TEXT, null=True, blank=True)
    meta_keywords = models.TextField('Meta keywords', help_text=CEO_HELP_TEXT, null=True, blank=True)
    meta_robots = models.TextField('Meta robots', help_text=CEO_HELP_TEXT, null=True, blank=True)

    sorting = models.PositiveIntegerField('Сортировка', editable=False)

    def __str__(self):
        return f'Корневой раздел "{self.title}"' if self.is_root() else f'Раздел "{self.title}"'

    def is_root(self) -> bool:
        return not self.parent_section

    def level(self) -> int:
        counter, obj = 1, self
        while obj.parent_section:
            obj = obj.parent_section
            counter += 1
        return counter

    def active_product_set(self):
        return self.product_set.filter(active=True)

    def active_section_set(self):
        return self.section_set.filter(active=True)

    def menu_set(self):
        section_set = list(self.active_section_set()) + list(self.active_product_set())
        return section_set

    def ceo_context(self):
        return {'section': self.title}

    class Meta:
        indexes = (models.Index(fields=('active', 'parent_section')),
                   models.Index(fields=('show_at_homepage',)))
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

        ordering = ['sorting']


class Product(SortableMixin):
    CEO_HELP_TEXT = 'Оставьте поле пустым чтобы использовать стандартную маску.'

    title = models.CharField('Название товара/услуги', max_length=255)
    url = AutoSlugField(verbose_name='URL товара/услуги', help_text='Заполняется на основе поля "Название товара/услуги"', populate_from='title', unique=True, editable=True,
                        max_length=120)
    time_duration = models.CharField('Длительность выполнения', help_text='Заполняется текстом (пример: "2 часа")', max_length=63, null=True, blank=True)
    fixed_price = models.BooleanField('Фиксированная цена', help_text='Не фикскированная цена будет отображаться как "от 990₽"', default=False)
    price = models.FloatField('Цена за работу (₽)')

    short_description = models.CharField('Краткое описание', max_length=255, blank=True)
    description = models.TextField('Содержание страницы', help_text=SUPPORTS_CAR_CONTEXT_HELP_TEXT)

    active = models.BooleanField('Активно', help_text=ACTIVE_HELP_TEXT, default=True)
    section = models.ForeignKey(verbose_name='Родительский раздел', to='Section', on_delete=models.RESTRICT)
    show_at_homepage = models.BooleanField('Отображать на главной', help_text='В блоке "Наши услуги"', default=False)
    spare_parts = models.ManyToManyField(verbose_name='Запчасти', to='SparePart', blank=True)
    cars = OptimizedManyToManyField(verbose_name='Машины, подходящие под данный товар/услугу', to='cars.Modification', blank=True)
    tag = models.ForeignKey(verbose_name='Тег', to=Tag, on_delete=models.SET_NULL, null=True, blank=True)

    similar_products = models.ManyToManyField(verbose_name='Похожие услуги', help_text='Выводятся когда пользователь попал на услугу, которая не поддерживается его авто.',
                                              to='self', blank=True)

    image = models.ImageField('Изображение', help_text='Возможность обрезки появится после сохранения', upload_to='services/products', max_length=256)
    thumbnail_1960x600 = ImageRatioField(verbose_name='Обрезка изображения (1920x600)', help_text='Для фона заголовка страницы', image_field='image', size='1920x600')
    thumbnail_960x585 = ImageRatioField(verbose_name='Обрезка изображения (960x585)', image_field='image', size='960x585')
    thumbnail_455x200 = ImageRatioField(verbose_name='Обрезка изображения (455x200)', image_field='image', size='455x200')
    thumbnail_348x236 = ImageRatioField(verbose_name='Обрезка изображения (348x236)', image_field='image', size='348x236')
    thumbnail_268x118 = ImageRatioField(verbose_name='Обрезка изображения (268x118)', image_field='image', size='268x118')
    thumbnail_80x80 = ImageRatioField(verbose_name='Обрезка изображения (80x80)', image_field='image', size='80x80')

    show_in_promotions = models.BooleanField('В акциях', help_text='Отображать среди баннеров акций на главной', default=False)
    homepage_description = models.CharField('Краткое описание для списка акций главной страницы (до 500 символов)', max_length=500, blank=True)

    meta_title = models.CharField('Заголовок <title>', help_text=CEO_HELP_TEXT, max_length=200, blank=True)
    meta_header = models.CharField('Заголовок <h1>', help_text=CEO_HELP_TEXT, max_length=200, blank=True)
    meta_description = models.TextField('Meta description', help_text=CEO_HELP_TEXT, null=True, blank=True)
    meta_keywords = models.TextField('Meta keywords', help_text=CEO_HELP_TEXT, null=True, blank=True)
    meta_robots = models.TextField('Meta robots', help_text=CEO_HELP_TEXT, null=True, blank=True)
    canonical_to_original = models.BooleanField('Каноничная ссылка', help_text='Каноничная ссылка на страницу без ММП фильтра', default=False)

    sorting = models.PositiveIntegerField('Сортировка', editable=False)

    def __str__(self):
        return f'Товар/Услуга "{self.title}"'

    @display(description='Цена')
    def verbose_price(self):
        price = format_price(self.price, '₽')
        return f'{price}' if self.fixed_price else f'От {price}'

    def root_section(self):
        section = self.section
        while section.parent_section:
            section = section.parent_section
        return section

    def ceo_context(self):
        return {'section': self.section.title, 'product': self.title}

    @staticmethod
    def get_currency():
        return '₽'

    def reverse_url(self):
        return reverse('services:product', args=(self.url,))

    class Meta:
        indexes = (models.Index(fields=('active',)),
                   models.Index(fields=('show_at_homepage',)),
                   models.Index(fields=('section_id',)))
        verbose_name = 'Товар/Услуга'
        verbose_name_plural = 'Товары/Услуги'

        ordering = ['sorting']


class SparePart(models.Model):
    title = models.CharField('Название запчасти', max_length=255)
    url = AutoSlugField(verbose_name='URL запчасти', help_text='Заполняется на основе поля "Название запчасти"', populate_from='title', unique=True, editable=True, max_length=120)

    image = models.ImageField('Изображение', help_text='Возможность обрезки появится после сохранения', upload_to='services/spare_parts', max_length=256)
    thumbnail_268x118 = ImageRatioField(verbose_name='Обрезка изображения для картинки запчасти на странице услуги/товара (268x118)', image_field='image', size='268x118')

    price = models.FloatField('Цена за запчасть (₽)')
    fixed_price = models.BooleanField('Фиксированная цена', help_text='Не фикскированная цена будет отображаться как "от 990 руб."', default=False)

    def __str__(self):
        return f'Запчасть "{self.title}"'

    @display(description='Цена')
    def verbose_price(self):
        price = format_price(self.price, '₽')
        return f'{price}' if self.fixed_price else f'От {price}'

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'
