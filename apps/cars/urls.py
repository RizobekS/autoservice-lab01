from django.urls import path, register_converter

from .utils.urlconverters import CarPathConverter, OldCarPathConverter
from .views import ajax_filter, CarView, RedirectOldCarUrls

app_name = 'cars'

register_converter(CarPathConverter, 'car_converter')
register_converter(OldCarPathConverter, 'old_car_converter')

urlpatterns = [
    path('<old_car_converter:urls>/', RedirectOldCarUrls.as_view(), name='redirect_car_url'),

    path('ajax-filter/', ajax_filter, name='ajax-filter'),

    path('<car_converter:urls>/', CarView.as_view(), name='car'),
]
