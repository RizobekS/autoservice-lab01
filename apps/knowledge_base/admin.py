from django.contrib import admin
from django.utils.html import strip_tags

from apps.knowledge_base.forms import FaqEntryAdminForm
from apps.knowledge_base.models import FaqEntry, Symptom


@admin.register(FaqEntry)
class FaqEntryAdmin(admin.ModelAdmin):
    list_display = ('title_or_question', 'url', 'asking_name', 'tag_string', 'answered')
    list_filter = ('title', 'answered', 'master', 'tags', 'branch')
    search_fields = ('question', 'answer', 'asking_name', 'asking_email')

    prepopulated_fields = {'url': ('title',), }
    fields = (('title', 'url'), 'answer', ('asking_name', 'asking_email'), 'question', 'answered', 'tags', 'master', 'branch', 'date')

    form = FaqEntryAdminForm

    @admin.display(description='Вопрос')
    def title_or_question(self, obj):
        return obj.title if obj.title else obj.question

    @admin.display(description='Тэги')
    def tag_string(self, obj):
        return ', '.join(item.name for item in obj.tags.all())


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'tag_string', 'active')
    list_filter = ('active', 'master', 'tags', 'branch')
    search_fields = ('title', 'answer')

    prepopulated_fields = {'url': ('title',), }
    fields = (('title', 'url'), 'active', 'answer', 'tags', 'master', 'branch', 'date')

    form = FaqEntryAdminForm

    @admin.display(description='Тэги')
    def tag_string(self, obj):
        return ', '.join(item.name for item in obj.tags.all())
