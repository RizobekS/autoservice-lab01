from django.db.models import QuerySet
from django.views.generic.base import ContextMixin

from apps.knowledge_base.models import FaqEntry, Symptom


class FaqEntryListMixin(ContextMixin):
    """
        Adds FAQ list to your context, ordered by time in ascending manner

        queryset_faqentry: QuerySet - queryset to filter from
        context_name_faqentry: str - name of context variable
        max_faqentry: int - Number of FaqEntry to retrieve, None by default (infinity)
    """

    queryset_faqentry: QuerySet = FaqEntry.objects
    context_name_faqentry: str = 'faq_entry_list'
    max_faqentry: int = None

    def get_faqentry_queryset(self):
        return self.queryset_faqentry

    def get_faqentry_list(self):
        queryset = self.get_faqentry_queryset()
        queryset = queryset.filter(answered=True).exclude(url__isnull=True, url__exact='').order_by('-date').distinct()
        return queryset[:self.max_faqentry] if self.max_faqentry is not None else queryset

    def get_context_data(self, **kwargs):
        return super().get_context_data(**{self.context_name_faqentry: self.get_faqentry_list()}, **kwargs)


class SymptomListMixin(ContextMixin):
    """
        Adds Symptom list to your context, ordered by time in ascending manner

        queryset_symptom: QuerySet - queryset to filter from
        context_name_symptom: str - name of context variable
        max_symptom: int - Number of Symptom to retrieve, None by default (infinity)
    """

    queryset_symptom: QuerySet = Symptom.objects
    context_name_symptom: str = 'symptom_list'
    max_symptom: int = None

    def get_symptom_queryset(self):
        return self.queryset_symptom

    def get_symptom_list(self):
        queryset = self.get_symptom_queryset()
        queryset = queryset.filter(active=True).order_by('-date').distinct()
        return queryset[:self.max_symptom] if self.max_symptom is not None else queryset

    def get_context_data(self, **kwargs):
        return super().get_context_data(**{self.context_name_symptom: self.get_symptom_list()}, **kwargs)
