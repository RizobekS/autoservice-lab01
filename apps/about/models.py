from django.db import models


class EditorContent(models.Model):
    title = models.CharField('Описание', max_length=60)
    key = models.CharField('Ключ', max_length=20, unique=True, primary_key=True)
    text = models.TextField('Содержание блока', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блок страницы "О нас"'
        verbose_name_plural = 'Блоки страницы "О нас"'
