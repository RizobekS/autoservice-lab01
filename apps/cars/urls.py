from django.urls import path, register_converter

from . import views
from .utils.urlconverters import CarPathConverter

app_name = 'cars'

register_converter(CarPathConverter, 'car_converter')

urlpatterns = [
    path('ajax-filter/', views.ajax_filter, name='ajax-filter'),

    path('<car_converter:urls>/', views.car_view, name='car'),
]
