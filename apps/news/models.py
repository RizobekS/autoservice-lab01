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

CONDITIONS = (('editing', 'Редактирование'), ('pending', 'Ожидание'), ('published', 'Опубликовано'),)


class Article(models.Model):
    title = models.CharField('Заголовок статьи', max_length=500)
    url = AutoSlugField(verbose_name='URL статьи', unique=True, populate_from='title', editable=True, max_length=120)
    text = models.TextField('Контент')
    short_description = models.CharField('Краткое описание (до 250 символов)', help_text='Заполняется для страницы тегов', max_length=250)

    author = models.ForeignKey(verbose_name='Автор', to=Master, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(verbose_name='Тэги', to=Tag, blank=True)
    status = models.CharField('Статус статьи', help_text='Отображаться будут только статьи с статусом "Опубликовано"', default='editing', max_length=30, choices=CONDITIONS)
    date = models.DateTimeField("Дата создания")

    image = models.ImageField('Изображение статьи', help_text='Возможность обрезки появится после сохранения', upload_to='articles/', max_length=256)
    thumbnail = ImageRatioField(verbose_name='Обрезка изображения для страницы списка новостей (800x360)', image_field='image', size='800x360')
    icon_thumbnail = ImageRatioField(verbose_name='Обрезка изображения для списка "Последние записи" (100x100)', image_field='image', size='100x100')

    def __str__(self):
        return self.title

    def active(self):
        return self.status == 'published'

    def reverse_url(self):
        return reverse('knowledge_base:news:article', args=(self.url,))

    @display(description='Тэги')
    def tag_string(self):
        return ', '.join(item.name for item in self.tags.all())

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Like(models.Model):
    article = models.ForeignKey(verbose_name='Статья', to=Article, on_delete=models.CASCADE)
    session = models.ForeignKey(verbose_name='Сессия', to=Session, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'Лайк на статье "{self.article.title}"'


class Comment(models.Model):
    author = models.ForeignKey(verbose_name='Пользователь', to=AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name='Комментарий под статьёй', to=Article, on_delete=models.CASCADE)
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

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
