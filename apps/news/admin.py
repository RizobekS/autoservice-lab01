from django.contrib import admin
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import ngettext
from image_cropping import ImageCroppingMixin

from utils.admin_actions import clone
from utils.helpers import admin_reverse
from .forms import ArticleAdminForm
from .models import Article, Comment


@admin.register(Article)
class ArticleAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'status', 'url', 'date', 'tag_string', 'is_news')
    list_editable = ('status', 'is_news')
    list_filter = ('status', 'is_news', 'date', 'tags', 'author')
    search_fields = ('title', 'short_description', 'text', 'status', 'author__name')
    actions = ('make_published', 'make_pending', 'make_editing', clone)
    filter_horizontal = ('suitable_products', 'suitable_sections')

    prepopulated_fields = {'url': ('title',), }
    autocomplete_fields = ('tags',)
    fieldsets = (
        (None, {'fields': (('title', 'url'), 'is_news', 'author', 'tags', 'status', 'date', 'suitable_sections', 'suitable_products')}),
        ('Изображение', {'fields': ('image', 'thumbnail', 'icon_thumbnail'), 'classes': ['wide']}),
        ('Текст', {'fields': ('short_description', 'text'), 'classes': ['wide']}),
    )
    form = ArticleAdminForm

    @admin.display(description='Опубликовать')
    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, ngettext('%d статья была успешно опубликована.', '%d статей были успешно опубликованы.',
                                            updated) % updated, messages.SUCCESS)

    @admin.display(description='Перевести в режим ожидания')
    def make_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, ngettext('%d статья была успешно переведена в режим ожидания.', '%d статей были успешно переведены в режим ожидания.',
                                            updated) % updated, messages.SUCCESS)

    @admin.display(description='Перевести в режим редактирования')
    def make_editing(self, request, queryset):
        updated = queryset.update(status='editing')
        self.message_user(request, ngettext('%d статья была успешно переведена в режим редактирования.', '%d статей были успешно переведены в режим редактирования.',
                                            updated) % updated, messages.SUCCESS)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('admin_title', 'author_link', 'article_link', 'reply_to_link', 'deepcount', 'date', 'visible')
    list_filter = ('visible', 'date', 'article', 'author')

    @admin.display(description='')
    def admin_title(self, obj):
        return f'Комментарий #{obj.id}'

    @admin.display(description='Автор')
    def author_link(self, obj):
        return admin_reverse(obj.author, obj.author.get_full_name())

    @admin.display(description='Статья')
    def article_link(self, obj):
        return admin_reverse(obj.article, obj.article.title)

    @admin.display(description='Ответ на комментарий')
    def reply_to_link(self, obj):
        return admin_reverse(obj.reply_to, str(obj.reply_to)) if obj.reply_to else None

    @admin.display(description='Дочерних комментариев')
    def deepcount(self, obj):
        overall = obj.child_comments.count()
        for item in obj.child_comments:
            overall += item.deepcount()
            if overall >= 5:
                return '>5'
        return overall
