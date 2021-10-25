from autoslug import AutoSlugField
from django.db import models


class EditorPage(models.Model):
    title = models.CharField('Заголовок', help_text='Так-же является содержимым тега title', max_length=200)
    url = AutoSlugField('URL страницы', max_length=60, unique=True, primary_key=True)
    content = models.TextField('Содержимое страницы')
    active = models.BooleanField('Активно', help_text='Снимите галочку с "Активно" вместо удаления. Неактивные страницы не будут отображаться нигде, кроме админ панели',
                                 default=True)

    meta_description = models.TextField('Meta description', help_text='Страницы этого раздела админ панели имеют отдельные CEO настройки', null=True, blank=True)
    meta_keywords = models.TextField('Meta keywords', help_text='Страницы этого раздела админ панели имеют отдельные CEO настройки', null=True, blank=True)
    meta_robots = models.TextField('Meta robots', help_text='Страницы этого раздела админ панели имеют отдельные CEO настройки', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.url}/'

    class Meta:
        ordering = ['url']
        indexes = [models.Index(fields=('active', 'url'))]
        verbose_name = 'Страница с изменяемым контентом'
        verbose_name_plural = 'Страницы с изменяемым контентом'
