from autoslug import AutoSlugField
from django.db import models


class Tag(models.Model):
    name = models.CharField("Название тега", max_length=50)
    url = AutoSlugField(verbose_name='URL тега', unique=True, populate_from='name', editable=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
