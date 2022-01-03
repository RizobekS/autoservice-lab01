from autoslug import AutoSlugField
from django.contrib.admin import display
from django.contrib.sessions.models import Session
from django.db import models
from django.urls import reverse
from image_cropping import ImageRatioField

from apps.tags.models import Tag
from autoservice.settings.common import AUTH_USER_MODEL
from ..accounts.models import User
from ..masters.models import Master
from ..services.models import Product, Section

CONDITIONS = (('editing', 'Редактирование'), ('pending', 'Ожидание'), ('published', 'Опубликовано'),)
NEWS_OR_ARTICLE = ((True, 'Новость'), (False, 'Статья (База знаний)'))


# Used both at news page and in knowledge_base
class Article(models.Model):
    title = models.CharField('Заголовок статьи', max_length=500)
    url = AutoSlugField(verbose_name='URL статьи', unique=True, populate_from='title', editable=True, max_length=120)
    is_news = models.BooleanField('Отображать в', choices=NEWS_OR_ARTICLE, default=True)  # If True - record is displayed at news page, if False - in knowledge base
    text = models.TextField('Контент')
    short_description = models.CharField('Краткое описание (до 250 символов)', help_text='Заполняется для страницы тегов', max_length=250)

    author = models.ForeignKey(verbose_name='Автор', help_text='Оставьте поле пустым, чтобы не отображать блок автора', to=Master, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(verbose_name='Тэги', to=Tag, blank=True)
    status = models.CharField('Статус статьи', help_text='Отображаться будут только статьи с статусом "Опубликовано"', default='editing', max_length=30, choices=CONDITIONS)
    date = models.DateTimeField("Дата создания")

    suitable_sections = models.ManyToManyField(verbose_name='Подходящие разделы', to=Section, blank=True)
    suitable_products = models.ManyToManyField(verbose_name='Подходящие услуги', to=Product, blank=True)

    image = models.ImageField('Изображение статьи', help_text='Возможность обрезки появится после сохранения', upload_to='articles/', max_length=256)
    thumbnail = ImageRatioField(verbose_name='Обрезка изображения для страницы списка новостей (800x360)', image_field='image', size='800x360')
    icon_thumbnail = ImageRatioField(verbose_name='Обрезка изображения для списка "Последние записи" (100x100)', image_field='image', size='100x100')

    def __str__(self):
        return self.title

    def active(self):
        return self.status == 'published'

    def reverse_url(self):
        return reverse('knowledge_base:article', args=(self.url,))

    def get_absolute_url(self):
        return reverse('news:article' if self.is_news else 'knowledge_base:article', args=(self.url,))

    def active_suitable_section_set(self):
        return self.suitable_sections.filter(active=True)

    def active_suitable_product_set(self):
        return self.suitable_products.filter(active=True)

    @display(description='Тэги')
    def tag_string(self):
        return ', '.join(item.name for item in self.tags.all())

    class Meta:
        ordering = ['-date']
        verbose_name = 'Статья/Новость'
        verbose_name_plural = 'Статьи/Новости'


class Like(models.Model):
    article = models.ForeignKey(verbose_name='Статья/Новость', to=Article, on_delete=models.CASCADE)
    session = models.ForeignKey(verbose_name='Сессия', to=Session, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'Лайк на статье "{self.article.title}"'


class Comment(models.Model):
    author = models.ForeignKey(verbose_name='Пользователь', to=AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name='Статья/Новость', help_text='Статья/Новость, под которой был оставлен комментарий', to=Article, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(verbose_name='Ответ на комментарий', to='Comment', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField('Дата создания', auto_now_add=True)
    visible = models.BooleanField('Отображение', help_text='Снимите галочку вместо удаления.', default=True)

    text = models.CharField('Текст комментария', max_length=2000)

    def __str__(self):
        return f'Комментарий #{self.id}'

    def tag_id(self):  # ID to be used in id="" attribute
        return f'comment-{self.id}'

    @property
    def child_comments(self):
        return self.comment_set.filter(visible=True)

    @property
    def level(self):
        item, counter = self, 0
        while item.reply_to:
            item, counter = item.reply_to, counter + 1
        return counter

    @display(description='Дочерних комментариев')
    def deepcount(self):
        overall = self.child_comments.count()
        for item in self.child_comments:
            overall += item.deepcount()
            if overall >= 5:
                return '>5'
        return overall

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
