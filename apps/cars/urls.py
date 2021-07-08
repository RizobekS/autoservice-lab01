from django.urls import path, register_converter

from .utils.urlconverters import CarPathConverter
from .views import ajax_filter, CarView

app_name = 'cars'

register_converter(CarPathConverter, 'car_converter')

urlpatterns = [
    path('ajax-filter/', ajax_filter, name='ajax-filter'),

    path('<car_converter:urls>/', CarView.as_view(), name='car'),
]
