"""autoservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from haystack.generic_views import SearchView

from utils.views import StaticPageView

static_urlpatterns = [
    path('certificates/', StaticPageView.as_view(template_name='static/certificates.html', viewname='static:certificates'), name='certificates'),
    path('reviews/', StaticPageView.as_view(template_name='static/reviews.html', viewname='static:reviews'), name='reviews'),
]

urlpatterns = [
    path('', include('apps.home.urls', namespace='home')),
    path('cars/', include('apps.cars.urls', namespace='cars')),
    path('blog/', include('apps.news.urls', namespace='news')),
    path('specials/', include('apps.promotions.urls', namespace='promotions')),
    path('account/', include('apps.accounts.urls', namespace='accounts')),
    path('tags/', include('apps.tags.urls', namespace='tags')),
    path('knowledge-base/', include('apps.knowledge_base.urls', namespace='knowledge_base')),
    path('raboty/', include('apps.work_gallery.urls', namespace='work_gallery')),
    path('contacts/', include('apps.contacts.urls', namespace='contacts')),

    path('', include((static_urlpatterns, 'static'), namespace='static')),

    path('admin/', admin.site.urls),

    url(r'^search/$', SearchView.as_view(), name='haystack_search'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # This is the last one, because it can intercept other urls
    path('', include('apps.services.urls', namespace='services')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
