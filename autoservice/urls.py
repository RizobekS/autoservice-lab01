"""autoservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
# Django imports
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from haystack.generic_views import SearchView

urlpatterns = [
    path('', include('apps.home.urls', namespace='home')),
    path('cars/', include('apps.cars.urls', namespace='cars')),
    path('services/', include('apps.services.urls', namespace='services')),
    path('blog/', include('apps.news.urls', namespace='news')),
    path('specials/', include('apps.promotions.urls', namespace='promotions')),
    path('account/', include('apps.accounts.urls', namespace='accounts')),
    path('tags/', include('apps.tags.urls', namespace='tags')),
    path('knowledge-base/', include('apps.knowledge_base.urls', namespace='knowledge_base')),

    path('admin/', admin.site.urls),

    url(r'^search/$', SearchView.as_view(), name='haystack_search'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
