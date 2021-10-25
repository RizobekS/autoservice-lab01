from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField("Название тега", max_length=50)
    url = AutoSlugField(verbose_name='URL тега', unique=True, populate_from='name', editable=True, null=True, blank=True, max_length=120)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tags:single', args=(self.url,))

    class Meta:
        ordering = ['id']
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
