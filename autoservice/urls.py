"""autoservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.urls import path, include
from django.views.generic import TemplateView
from haystack.generic_views import SearchView

from autoservice.sitemap.sitemap import sitemaps
from utils.views import StaticPageView

static_urlpatterns = [
    path('certificates/', StaticPageView.as_view(template_name='static/certificates.html', viewname='static:certificates'), name='certificates'),
    path('yandex_808db4c62533456a.html', TemplateView.as_view(template_name='static/yandex_808db4c62533456a.html'), name='yandex_verification_key'),
]

urlpatterns = [
    path('sitemap.xml', sitemap_views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', sitemap_views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('', include('apps.home.urls', namespace='home')),
    path('cars/', include('apps.cars.urls', namespace='cars')),
    path('specials/', include('apps.promotions.urls', namespace='promotions')),
    path('account/', include('apps.accounts.urls', namespace='accounts')),
    path('tags/', include('apps.tags.urls', namespace='tags')),
    path('raboty/', include('apps.work_gallery.urls', namespace='work_gallery')),
    path('contacts/', include('apps.contacts.urls', namespace='contacts')),
    path('about/', include('apps.about.urls', namespace='about')),
    path('news/', include('apps.news.urls', namespace='news')),
    path('', include('apps.knowledge_base.urls', namespace='knowledge_base')),

    path('', include((static_urlpatterns, 'static'), namespace='static')),

    path('admin/', admin.site.urls),

    url(r'^search/$', SearchView.as_view(), name='haystack_search'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # This is the last one, because it can intercept other urls
    path('', include('apps.services.urls', namespace='services')),
    path('pages/', include('apps.editor_pages.urls', namespace='editor_pages')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.site_settings.views.handler404'
