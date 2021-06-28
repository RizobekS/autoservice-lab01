from django.urls import path, register_converter
from . import views
from ..cars.utils.urlconverters import CarPathConverter

app_name = 'services'

register_converter(CarPathConverter, 'car_converter')

urlpatterns = [
    path('<str:section_url>/', views.section_view, name='section'),
    path('<str:section_url>/<car_converter:urls>/', views.section_view, name='section_car'),
    path('<str:section_url>/<str:product_url>/', views.product_view, name='product'),
    path('<str:section_url>/<str:product_url>/<car_converter:urls>/', views.product_view, name='product_car'),
]
