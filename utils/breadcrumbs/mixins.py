from typing import List, Dict, Any, Union

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.views.generic.base import ContextMixin

from utils.breadcrumbs.types import Breadcrumb


class BreadcrumbsMixin(ContextMixin):
    """
        Automatically updates context with "breadcrumbs" variable.
        This mixin is designed to be extended by View

        initial_breadcrumbs: List[Breadcrumb] - initial value for your breadcrumbs
        extra_breadcrumbs: List[Breadcrumb] or Breadcrumb - appears at the end of breadcrumbs list
    """
    _breadcrumbs: List[Breadcrumb] = []
    initial_breadcrumbs: List[Breadcrumb] = []
    extra_breadcrumbs: Union[List[Breadcrumb], Breadcrumb] = None

    def get_initial_breadcrumbs(self):
        return self.initial_breadcrumbs

    def get_breadcrumbs(self) -> List[Breadcrumb]:
        breadcrumbs = self.get_initial_breadcrumbs() + self._breadcrumbs
        if self.extra_breadcrumbs:
            if isinstance(self.extra_breadcrumbs, list):
                breadcrumbs = breadcrumbs + self.extra_breadcrumbs
            else:
                breadcrumbs.append(self.extra_breadcrumbs)
        return breadcrumbs

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context


class PageTitleMixin(BreadcrumbsMixin):
    """
        Extends BreadcrumbsMixin and adds additional breadcrumb using page_title context variable

        viewname: str - view name for constructing reverse url
        page_title_context_name: str - name of context variable
        page_title: str - page title
    """
    viewname: str = None
    page_title: str = None
    page_title_context_name: str = 'page_title'

    def get_page_title(self):
        if self.page_title is None:
            raise ImproperlyConfigured('Please set page_title variable from PageTitleMixin')
        return self.page_title

    def get_initial_breadcrumbs(self):
        return self.initial_breadcrumbs + [Breadcrumb(self.get_page_title(), '#' if self.viewname is None else reverse_lazy(self.viewname))]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.page_title_context_name] = self.get_page_title()
        return context
