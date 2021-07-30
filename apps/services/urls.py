from django.urls import path, register_converter

from .utils.urlconverters import SectionUrlFilter
from .views import SectionView, ProductView
from ..cars.utils.urlconverters import CarPathConverter

app_name = 'services'

register_converter(CarPathConverter, 'car_converter')
register_converter(SectionUrlFilter, 'section_filter')

urlpatterns = [
    path('<section_filter:section_url>/', SectionView.as_view(), name='section'),
    path('<str:product_url>/', ProductView.as_view(), name='product'),
    path('<section_filter:section_url>/<car_converter:urls>/', SectionView.as_view(), name='section_car'),
    path('<str:product_url>/<car_converter:urls>/', ProductView.as_view(), name='product_car'),
]
