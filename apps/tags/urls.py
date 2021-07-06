from django.urls import path

from .views import *

app_name = 'tags'

urlpatterns = [
    path('', TagsListView.as_view(), name='all'),
    path('<str:tag>/', TagsListView.as_view(), name='single'),
]
