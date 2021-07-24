from typing import Any, Dict

from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.utils.html import strip_tags
from django.views.generic import CreateView, DetailView, TemplateView

from apps.knowledge_base.forms import AskQuestionForm
from apps.knowledge_base.models import FaqEntry, Symptom
from apps.knowledge_base.utils.mixins import FaqEntryListMixin, SymptomListMixin
from apps.tags.models import Tag
from utils.breadcrumbs.utils import reverse_bc
from utils.mixins import PageSettingsMixin


class KnowledgeBaseView(TemplateView, PageSettingsMixin, FaqEntryListMixin, SymptomListMixin):
    template_name = 'knowledge_base/knowledge-base.html'
    viewname = 'knowledge_base:list'

    max_articles = None
    context_name_faqentry = 'faq_entries'
    context_name_symptom = 'symptoms'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        all_records = [*context.get('faq_entries'), *context.get('symptoms')]
        all_records.sort(key=lambda item: item.date, reverse=True)
        context.update({
            'all_records': all_records,
            'tags': Tag.objects.filter(Q(faqentry__isnull=False) | Q(symptom__isnull=False)).distinct()
        })
        return context


class AnsweredQuestionView(CreateView, PageSettingsMixin, FaqEntryListMixin):
    template_name = 'knowledge_base/answered-question.html'
    model = FaqEntry
    form_class = AskQuestionForm
    faq_entry = None

    viewname = 'knowledge_base:answered-question'
    initial_breadcrumbs = [reverse_bc(viewname=KnowledgeBaseView.viewname)]

    def get_ceo_context(self) -> Dict[str, Any]:
        context = super().get_ceo_context()
        context.update({'title': self.faq_entry.title, 'answer': strip_tags(self.faq_entry.answer)})
        return context

    def get_page_title(self):
        return self.faq_entry.title

    context_name_faqentry = 'related'

    def get_faqentry_queryset(self):
        return FaqEntry.objects.filter(tags__in=self.faq_entry.tags.all()).exclude(id=self.faq_entry.id)

    def get_faqentry_list(self):
        result = super().get_faqentry_list()
        tag_set = set(self.faq_entry.tags.all())
        return sorted(result, key=lambda item: len(set(item.tags.all()).intersection(tag_set)))

    def dispatch(self, request, *args, **kwargs):
        self.faq_entry = self.get_faq_entry()
        self.extra_context = {'faq_entry': self.faq_entry}
        result = super().dispatch(request, *args, **kwargs)
        return result

    def form_valid(self, form):
        messages.success(self.request, 'Вопрос был успешно добавлен ✔', extra_tags='text-success')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path_info

    def get_faq_entry(self):
        url = self.kwargs.get('url')
        faq_entry = FaqEntry.objects.filter(url__exact=url, answered=True).first()
        if faq_entry is None or url is None:
            raise Http404('Вопрос не найден')
        return faq_entry


class SymptomView(DetailView, PageSettingsMixin, SymptomListMixin):
    template_name = 'knowledge_base/symptom.html'
    queryset = Symptom.objects.filter(active=True)

    slug_field = 'url'
    slug_url_kwarg = 'url'
    context_object_name = 'symptom'

    viewname = 'knowledge_base:symptom'
    initial_breadcrumbs = [reverse_bc(viewname=KnowledgeBaseView.viewname)]

    def get_ceo_context(self) -> Dict[str, Any]:
        context = super().get_ceo_context()
        context.update({'title': self.object.title, 'answer': strip_tags(self.object.answer)})
        return context

    def get_page_title(self):
        return self.object.title

    context_name_symptom = 'related'

    def get_symptom_queryset(self):
        return Symptom.objects.filter(tags__in=self.object.tags.all()).exclude(id=self.object.id)

    def get_symptom_list(self):
        result = super().get_symptom_list()
        tag_set = set(self.object.tags.all())
        return sorted(result, key=lambda item: len(set(item.tags.all()).intersection(tag_set)))

    def get(self, *args, **kwargs):
        obj = self.get_object()
        related = Symptom.objects.filter(tags__in=obj.tags.all(), active=True).exclude(id=obj.id).distinct()
        self.extra_context = {
            'related': related,
        }
        return super().get(*args, **kwargs)
