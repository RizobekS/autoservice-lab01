from autoslug import AutoSlugField
from django.contrib.admin import display
from django.db import models

from image_cropping import ImageRatioField

from apps.cars.utils.validators import validate_double_slash_url
from apps.services.utils.help_text import DESCRIPTION_HELP_TEXT, TITLE_DATIVE_HELP_TEXT, ACTIVE_HELP_TEXT, VENDOR_PAGE_THUMBNAIL_HELP_TEXT
from utils.helpers import format_price


class Section(models.Model):
    # Common fields
    title = models.CharField('Название раздела', max_length=255)
    url = AutoSlugField(verbose_name='URL раздела', help_text='Заполняется на основе поля "Название раздела"',
                        validators=[validate_double_slash_url], populate_from='title', unique=True, editable=True)
    title_dative = models.CharField('Название раздела в Дательном падеже', help_text=TITLE_DATIVE_HELP_TEXT, max_length=255)
    active = models.BooleanField('Активно', help_text=ACTIVE_HELP_TEXT, default=True)
    short_description = models.CharField('Краткое описание', max_length=255)
    description = models.TextField('Содержание', help_text=DESCRIPTION_HELP_TEXT)
    image = models.ImageField('Изображение', help_text='Возможность обрезки появится после сохранения', upload_to='services/sections')
    title_background = ImageRatioField(verbose_name="Обрезка изображения для фона заголовка", image_field='image', size='1920x600')
    vendor_page_thumbnail = ImageRatioField(verbose_name="Обрезка изображения для страницы марки", help_text=VENDOR_PAGE_THUMBNAIL_HELP_TEXT, image_field='image', size='960x585')

    # != 1 section level fields
    parent_section = models.ForeignKey(verbose_name='Родительский раздел', to='Section', help_text='Оставьте поле пустым, если данный раздел - корневой',
                                       on_delete=models.SET_NULL, null=True, blank=True)
    card_thumbnail = ImageRatioField(verbose_name="Обрезка изображения для превью на странице раздела 1 уровня", image_field='image', size='455x200')

    # Appearing on homepage
    home_page = models.BooleanField('Отображать в блоке услуг/товаров на главной', default=False)
    homepage_thumbnail = ImageRatioField(verbose_name="Обрезка изображения для превью на главной странице", image_field='image', size='348x236')

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

    @display(description='Дочерние товары/услуги')
    def child_products(self) -> str:
        child_products = self.product_set
        return f'({child_products.count()}) {", ".join(section.title for section in child_products.all())}'

    @display(description='Уровень раздела')
    def verbose_level(self) -> str:
        if self.is_root():
            return 'Корневой'
        else:
            return f'{self.level()} уровня'

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Product(models.Model):
    title = models.CharField('Название товара/услуги', max_length=255)
    url = AutoSlugField(verbose_name='URL товара/услуги', help_text='Заполняется на основе поля "Название товара/услуги"', populate_from='title', unique=True, editable=True)
    active = models.BooleanField('Активно', help_text=ACTIVE_HELP_TEXT, default=True)
    section = models.ForeignKey(verbose_name='Родительский раздел', to='Section', on_delete=models.RESTRICT)
    short_description = models.CharField('Краткое описание', max_length=255, blank=True)
    description = models.TextField('Содержание страницы')
    time_duration = models.CharField('Длительность выполнения', help_text='Заполняется текстом (пример: "2 часа")', max_length=63)
    fixed_price = models.BooleanField('Фиксированная цена', help_text='Не фикскированная цена будет отображаться как "от 990₽"', default=False)
    price = models.FloatField('Цена за работу (₽)')

    image = models.ImageField('Изображение', help_text='Возможность обрезки появится после сохранения', upload_to='services/products')
    product_thumbnail = ImageRatioField(verbose_name="Обрезка изображения для картинки товара/услуги на странице услуги/товара", image_field='image', size='268x118')
    car_thumbnail = ImageRatioField(verbose_name="Обрезка изображения для картинки товара/услуги на странице автомобиля (ММ и выше)", image_field='image', size='268x268')
    icon_thumbnail = ImageRatioField(verbose_name="Обрезка изображения для превью в списке товаров/услуг", image_field='image', size='80x80')

    spare_parts = models.ManyToManyField(verbose_name='Запчасти', to='SparePart', blank=True)
    cars = models.ManyToManyField(verbose_name='Машины, подходящие под данный товар/услугу', to='cars.Modification', blank=True)

    # Appearing on homepage
    home_page = models.BooleanField('Отображать в блоке услуг/товаров на главной', default=False)
    homepage_thumbnail = ImageRatioField(verbose_name="Обрезка изображения для превью на главной странице", image_field='image', size='348x236')

    # Appearing in favourites
    is_favourite = models.BooleanField('Отображать в блоке избранных услуг/товаров', help_text='Избранные услуги/товары отображаются в соответствующем блоке на главной странице',
                                       default=False)
    favourite_text = models.TextField('Текст избранной услуги/товара', help_text='Небольшой текст с поддержкой html, который будет отображаться под ценой '
                                                                                 'услуги/товара на главной', null=True, blank=True)

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

    class Meta:
        verbose_name = 'Товар/Услуга'
        verbose_name_plural = 'Товары/Услуги'


class SparePart(models.Model):
    title = models.CharField('Название запчасти', max_length=255)
    url = AutoSlugField(verbose_name='URL раздела', help_text='Заполняется на основе поля "Название запчасти"', populate_from='title', unique=True, editable=True)

    image = models.ImageField('Изображение', help_text='Возможность обрезки появится после сохранения', upload_to='services/spare_parts')
    product_thumbnail = ImageRatioField(verbose_name="Обрезка изображения для картинки запчасти на странице услуги/товара", image_field='image', size='268x118')

    price = models.FloatField('Цена за запчасть (₽)')
    fixed_price = models.BooleanField('Фиксированная цена', help_text='Не фикскированная цена будет отображаться как "от 990 руб."', default=False)

    def __str__(self):
        return f'Запчасть "{self.title}"'

    @display(description='Цена')
    def verbose_price(self):
        return f'От {self.price}₽' if self.fixed_price else f'{self.price}₽'

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'
