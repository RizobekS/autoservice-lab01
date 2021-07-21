from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse

from apps.masters.models import Master
from apps.site_settings.models import Branch
from apps.tags.models import Tag


class FaqEntry(models.Model):
    title = models.CharField('Название вопроса', max_length=128, null=True, blank=True)
    url = AutoSlugField(verbose_name='URL вопроса', unique=True, populate_from='title', editable=True, null=True, blank=True)
    answered = models.BooleanField('Отвечен', help_text='Неотвеченные вопросы не отображаются нигде, кроме админки', default=False)
    question = models.CharField('Вопрос', max_length=1024)
    answer = models.CharField('Ответ', max_length=2048, null=True, blank=True)
    tags = models.ManyToManyField(verbose_name='Теги', to=Tag, blank=True)
    date = models.DateTimeField('Дата и время', null=True, blank=True)

    asking_name = models.CharField('Имя спрашивающего', max_length=128)
    asking_email = models.EmailField('Эл. почта спрашивающего', null=True, blank=True)

    master = models.ForeignKey(verbose_name='Отвечающий', to=Master, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(verbose_name='Филиал (Отвечающий)', to=Branch, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title if self.title else self.question

    def reverse_url(self):
        return reverse('knowledge_base:answered-question', args=(self.url,))

    class Meta:
        verbose_name = 'Вопрос/Ответ'
        verbose_name_plural = 'Вопросы/Ответы'


class Symptom(models.Model):
    title = models.CharField('Название симптома', max_length=256)
    url = AutoSlugField(verbose_name='URL симптома', unique=True, populate_from='title', editable=True)
    active = models.BooleanField('Отвечен', help_text='Неотвеченные симптомы не отображаются нигде, кроме админки', default=True)
    answer = models.CharField('Ответ', max_length=2048)
    tags = models.ManyToManyField(verbose_name='Теги', to=Tag, blank=True)
    date = models.DateTimeField('Дата и время')

    master = models.ForeignKey(verbose_name='Отвечающий', to=Master, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(verbose_name='Филиал (Отвечающий)', to=Branch, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def reverse_url(self):
        return reverse('knowledge_base:symptom', args=(self.url,))

    class Meta:
        verbose_name = 'Симптом'
        verbose_name_plural = 'Симптомы'
