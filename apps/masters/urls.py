from django.urls import path

from .views import AboutMastersView

app_name = 'masters'

urlpatterns = [
    path('', AboutMastersView.as_view(), name='about')
]
