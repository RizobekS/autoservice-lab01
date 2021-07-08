from typing import List, Dict, Any

from django.views.generic.base import ContextMixin

from utils.breadcrumbs.types import Breadcrumb


class BreadcrumbsMixin(ContextMixin):
    """
        Automatically updates context with "breadcrumbs" variable.
        This mixin is designed to be extended by View

        initial_breadcrumbs: List[Breadcrumb] - initial value for your breadcrumbs
        current_breadcrumb: Breadcrumb = breadcrumb for current view
    """
    initial_breadcrumbs: List[Breadcrumb] = []
    current_breadcrumb: Breadcrumb = None

    def get_initial_breadcrumbs(self) -> List[Breadcrumb]:
        return self.initial_breadcrumbs

    def get_current_breadcrumb(self) -> List[Breadcrumb]:
        return [self.current_breadcrumb] if self.current_breadcrumb else []

    def get_breadcrumbs(self) -> List[Breadcrumb]:
        return self.get_initial_breadcrumbs() + self.get_current_breadcrumb()

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        kwargs['breadcrumbs'] = self.get_breadcrumbs()
        return super().get_context_data(**kwargs)
