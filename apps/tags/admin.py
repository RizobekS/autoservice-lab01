from django.contrib import admin

from apps.tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'article_string', 'promotions_string', 'product_string')
    search_fields = ('name', 'url')

    prepopulated_fields = {'url': ('name',), }

    @admin.display(description='Статьи')
    def article_string(self):
        return f'({self.article_set.count()}) {" ,  ".join(item.title for item in self.article_set.all())}'

    @admin.display(description='Акции')
    def promotions_string(self):
        return f'({self.promotion_set.count()}) {" ,  ".join(item.title for item in self.promotion_set.all())}'

    @admin.display(description='Товары/Услуги')
    def product_string(self):
        return f'({self.product_set.count()}) {" ,  ".join(item.title for item in self.product_set.all())}'
