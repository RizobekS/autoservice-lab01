from django.contrib import admin

from apps.tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'article_string', 'promotions_string')
    search_fields = ('name', 'url')

    prepopulated_fields = {'url': ('name',), }
