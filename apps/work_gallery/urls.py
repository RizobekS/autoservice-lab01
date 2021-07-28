from django.urls import path

from apps.work_gallery.views import WorkGalleryView, SingleWorkView

app_name = 'work_gallery'

urlpatterns = [
    path('', WorkGalleryView.as_view(), name='list'),
    path('<str:work_url>/', SingleWorkView.as_view(), name='single'),
]
