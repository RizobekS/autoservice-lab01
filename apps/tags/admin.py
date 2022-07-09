from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.tags.models import Tag
from utils.helpers import admin_reverse


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name', 'url', 'article_string', 'promotions_string', 'product_string', 'faqentry_string', 'symptom_string')
    readonly_fields = ('article_string', 'promotions_string', 'product_string', 'faqentry_string', 'symptom_string')
    list_display = ('name', 'url', 'all_tied_records_string')
    search_fields = ('name', 'url')

    prepopulated_fields = {'url': ('name',), }

    @admin.display(description='Привязанные записи')
    def all_tied_records_string(self, obj):
        article_set = [admin_reverse(item, item.title) for item in obj.article_set.all()]
        promotion_set = [admin_reverse(item, item.title) for item in obj.promotion_set.all()]
        product_set = [admin_reverse(item, item.title) for item in obj.product_set.all()]
        faqentry_set = [admin_reverse(item, item.title) for item in obj.faqentry_set.all()]
        symptom_set = [admin_reverse(item, item.title) for item in obj.symptom_set.all()]
        mix = article_set + promotion_set + product_set + faqentry_set + symptom_set
        return mark_safe(f'({len(mix)}) {" ,  ".join(mix)}')

    @admin.display(description='Привязанные Статьи')
    def article_string(self, obj):
        return mark_safe(f'({obj.article_set.count()}) {" ,  ".join(admin_reverse(item, item.title) for item in obj.article_set.all())}')

    @admin.display(description='Привязанные Акции')
    def promotions_string(self, obj):
        return mark_safe(f'({obj.promotion_set.count()}) {" ,  ".join(admin_reverse(item, item.title) for item in obj.promotion_set.all())}')

    @admin.display(description='Привязанные Товары/Услуги')
    def product_string(self, obj):
        return mark_safe(f'({obj.product_set.count()}) {" ,  ".join(admin_reverse(item, item.title) for item in obj.product_set.all())}')

    @admin.display(description='Привязанные Вопросы/Ответы')
    def faqentry_string(self, obj):
        return mark_safe(f'({obj.faqentry_set.count()}) {" ,  ".join(admin_reverse(item, item.title) for item in obj.faqentry_set.all())}')

    @admin.display(description='Привязанные Симптомы')
    def symptom_string(self, obj):
        return mark_safe(f'({obj.symptom_set.count()}) {" ,  ".join(admin_reverse(item, item.title) for item in obj.symptom_set.all())}')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('article_set', 'promotion_set', 'product_set', 'faqentry_set', 'symptom_set')
