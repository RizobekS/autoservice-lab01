from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from image_cropping import ImageCroppingMixin

from .forms import ArticleAdminForm
from .models import *


@admin.register(Article)
class ArticleAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'status', 'url', 'date', 'short_description', 'tag_string')
    list_editable = ('status',)
    list_filter = ('status', 'date', 'tags', 'author')
    search_fields = ('title', 'short_description', 'text', 'status', 'author__name')
    actions = ('make_published', 'make_pending', 'make_editing')

    prepopulated_fields = {'url': ('title',), }
    autocomplete_fields = ('tags',)
    fieldsets = (
        (None, {'fields': (('title', 'url'), 'author', 'tags', 'status', 'date')}),
        ('Изображение', {'fields': ('image', 'thumbnail', 'icon_thumbnail'), 'classes': ['wide']}),
        ('Текст', {'fields': ('short_description', 'text'), 'classes': ['wide']}),
    )
    form = ArticleAdminForm

    @display(description='Опубликовать')
    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, ngettext('%d статья была успешно опубликована.', '%d статей были успешно опубликованы.',
                                            updated) % updated, messages.SUCCESS)

    @display(description='Перевести в режим ожидания')
    def make_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, ngettext('%d статья была успешно переведена в режим ожидания.', '%d статей были успешно переведены в режим ожидания.',
                                            updated) % updated, messages.SUCCESS)

    @display(description='Перевести в режим редактирования')
    def make_editing(self, request, queryset):
        updated = queryset.update(status='editing')
        self.message_user(request, ngettext('%d статья была успешно переведена в режим редактирования.', '%d статей были успешно переведены в режим редактирования.',
                                            updated) % updated, messages.SUCCESS)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('admin_title', 'author_link', 'article_link', 'reply_to_link', 'deepcount', 'date', 'visible')
    list_filter = ('visible', 'date', 'article', 'author')
