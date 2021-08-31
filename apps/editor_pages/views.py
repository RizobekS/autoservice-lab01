from typing import List

from django.views.generic import DetailView

from apps.editor_pages.models import EditorPage
from utils.breadcrumbs.mixins import BreadcrumbsMixin
from utils.breadcrumbs.types import Breadcrumb


class EditorPageView(DetailView, BreadcrumbsMixin):
    url: str = None
    template_name = 'editor_pages/editor_page.html'

    def get_object(self, queryset=None):
        return EditorPage.objects.get(active=True, url=self.url)

    def get_current_breadcrumb(self) -> List[Breadcrumb]:
        return [Breadcrumb(self.object.title, '#')]

    def get_context_data(self, **kwargs):
        # Add CEO data into context
        kwargs.update({
            'page_title': self.object.title,
            'meta_description': self.object.meta_description,
            'meta_keywords': self.object.meta_keywords,
            'meta_robots': self.object.meta_robots,
        })
        return super().get_context_data(**kwargs)
