from django.urls import path, register_converter

from utils.urlconverters import url_converter_factory
from .models import Section, Product
from .views import SectionView, ProductView, SparePartsView, SubmitCallRequestView
from ..cars.utils.urlconverters import CarPathConverter

app_name = 'services'

SectionUrlFilter = url_converter_factory(Section)
ProductUrlFilter = url_converter_factory(Product)

register_converter(CarPathConverter, 'car_converter')
register_converter(SectionUrlFilter, 'section_filter')
register_converter(ProductUrlFilter, 'product_filter')

urlpatterns = [
    path('spare-parts/', SparePartsView.as_view(), name='spare_parts'),
    path('call-request-form/', SubmitCallRequestView.as_view(), name='submit_call_request'),
    path('<section_filter:section_url>/', SectionView.as_view(), name='section'),
    path('<product_filter:product_url>/', ProductView.as_view(), name='product'),
    path('<section_filter:section_url>/<car_converter:urls>/', SectionView.as_view(), name='section_car'),
    path('<product_filter:product_url>/<car_converter:urls>/', ProductView.as_view(), name='product_car'),
]
