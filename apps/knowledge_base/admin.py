from django.contrib import admin

from apps.knowledge_base.forms import FaqEntryAdminForm
from apps.knowledge_base.models import FaqEntry, Symptom
from utils.admin_actions import clone


@admin.register(FaqEntry)
class FaqEntryAdmin(admin.ModelAdmin):
    list_display = ('title_or_question', 'url', 'asking_name', 'tag_string', 'answered')
    list_filter = ('title', 'answered', 'master', 'tags')
    search_fields = ('question', 'answer', 'asking_name', 'asking_email')
    actions = (clone,)

    prepopulated_fields = {'url': ('title',), }
    fields = (('title', 'url'), 'answer', ('asking_name', 'asking_email'), 'question', 'answered', 'tags', 'master', 'date')

    form = FaqEntryAdminForm

    @admin.display(description='Вопрос')
    def title_or_question(self, obj):
        return obj.title if obj.title else obj.question

    @admin.display(description='Тэги')
    def tag_string(self, obj):
        return ', '.join(item.name for item in obj.tags.all())

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'tag_string', 'active')
    list_filter = ('active', 'master', 'tags')
    search_fields = ('title', 'answer')
    actions = (clone,)

    prepopulated_fields = {'url': ('title',), }
    fields = (('title', 'url'), 'active', 'answer', 'tags', 'master', 'date')

    form = FaqEntryAdminForm

    @admin.display(description='Тэги')
    def tag_string(self, obj):
        return ', '.join(item.name for item in obj.tags.all())

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')
