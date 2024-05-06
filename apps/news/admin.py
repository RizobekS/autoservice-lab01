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

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('admin_title', 'author_link', 'article_link', 'reply_to_link', 'deepcount', 'date', 'visible')
    list_filter = ('visible', 'date', 'article')
    actions = ('hide', 'reveal')
    list_per_page = 10_000

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

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'article', 'reply_to')

    @admin.display(description='Скрыть')
    def hide(self, request, queryset):
        updated = queryset.update(visible=False)
        self.message_user(request, ngettext('%d комментарий был успешно скрыт.', '%d комментариев были успешно скрыты.',
                                            updated) % updated, messages.SUCCESS)

    @admin.display(description='Сделать видимыми')
    def reveal(self, request, queryset):
        updated = queryset.update(visible=True)
        self.message_user(request, ngettext('%d комментарий был успешно сделан видимым.', '%d комментариев были успешно сделаны видимыми.',
                                            updated) % updated, messages.SUCCESS)
