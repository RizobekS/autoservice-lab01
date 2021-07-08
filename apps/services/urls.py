from django.urls import path, register_converter

from .views import SectionView, ProductView
from ..cars.utils.urlconverters import CarPathConverter

app_name = 'services'

register_converter(CarPathConverter, 'car_converter')

urlpatterns = [
    path('<str:section_url>/', SectionView.as_view(), name='section'),
    path('<str:section_url>/<car_converter:urls>/', SectionView.as_view(), name='section_car'),
    path('<str:section_url>/<str:product_url>/', ProductView.as_view(), name='product'),
    path('<str:section_url>/<str:product_url>/<car_converter:urls>/', ProductView.as_view(), name='product_car'),
]
