from autoslug import AutoSlugField
from django.contrib.admin import display
from django.db import models


class Tag(models.Model):
    name = models.CharField("Название тега", max_length=50)
    url = AutoSlugField(verbose_name='URL тега', unique=True, populate_from='name', editable=True, null=True, blank=True)

    def __str__(self):
        return self.name

    @display(description='Статьи')
    def article_string(self):
        return f'({self.article_set.count()}) {" ,  ".join(item.title for item in self.article_set.all())}'

    @display(description='Акции')
    def promotions_string(self):
        return f'({self.promotion_set.count()}) {" ,  ".join(item.title for item in self.promotion_set.all())}'

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
