from typing import Any, Dict

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.template import Template, Context
from django.views.generic.base import ContextMixin

from apps.site_settings.models import CEOSetting, Branch


class CEORenderer:
    """
        Has methods to render page title and "description", "keywords", "robots"  meta tags
        Subclasses MUST implement ceo_key attribute and either ceo_context or get_ceo_context()
        get_ceo_context() must return context dictionary

        ceo_key: str - A key to find corresponding CEOSetting database entry
        ceo_context: Dict[str, Any] - variables, that are used to render meta tags and title
    """
    ceo_key = None
    ceo_context = {}

    def __init__(self, ceo_key=None, ceo_context={}):
        self.ceo_key = ceo_key
        self.ceo_context = ceo_context

    def _render(self, field_name):
        ceo_object = self.get_ceo_object()
        text = getattr(ceo_object, field_name)

        if text and ceo_object.variables:
            template = Template(f'{{% autoescape off %}}{text}{{% endautoescape %}}')
            return template.render(Context(self.get_ceo_context())).strip()
        else:
            return text.strip()

    def get_ceo_key(self):
        if self.ceo_key is None:
            raise ImproperlyConfigured('You must implement ceo_key attribute')
        return self.ceo_key

    def get_ceo_object(self) -> CEOSetting:
        key = self.get_ceo_key()
        ceo_obj = CEOSetting.objects.filter(key=key)
        if not ceo_obj.exists():
            raise ImproperlyConfigured(f'CEOSetting with key={key} does not exist')
        return ceo_obj.first()

    def get_ceo_context(self) -> Dict[str, Any]:
        return self.ceo_context

    def get_page_title(self):
        return self._render('title')

    def get_meta_description(self):
        return self._render('description')

    def get_meta_keywords(self):
        return self._render('keywords')

    def get_meta_robots(self):
        return self._render('robots')

    def as_context(self):
        return {
            'page_title': self.get_page_title(),
            'meta_description': self.get_meta_description(),
            'meta_keywords': self.get_meta_keywords(),
            'meta_robots': self.get_meta_robots(),
        }


class CEOMixin(ContextMixin, CEORenderer):
    """
        Adds meta_description, meta_keywords and meta_robots to your context
        overrides get_ceo_key() to fallback to viewname if available
    """

    def get_ceo_key(self):
        return self.viewname if hasattr(self, 'viewname') and self.viewname else super().get_ceo_key()

    def get_context_data(self, **kwargs):
        kwargs.update(self.as_context())
        return super().get_context_data(**kwargs)


class BranchesMixin(ContextMixin):
    """
        Adds list of branches into your context

        branches_context_name: str - context name of variable to hold branch list. Defaults to 'branches'
        branches_max: int - maximum number of branches. Defaults to infinity
        branches_queryset: QuerySet - queryset to retrieve branches from. Defaults to Branch.objects
    """
    branches_context_name: str = 'branches'
    branches_max: int = None
    branches_queryset: QuerySet = Branch.objects

    def get_branch_queryset(self):
        return self.branches_queryset

    def get_branch_list(self):
        queryset = self.get_branch_queryset()
        queryset = queryset.filter(active=True)
        return queryset[:self.branches_max] if self.branches_max else queryset

    def get_context_data(self, **kwargs):
        return super().get_context_data(**{self.branches_context_name: self.get_branch_list()}, **kwargs)
