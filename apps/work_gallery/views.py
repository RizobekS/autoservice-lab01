from typing import Any, Dict

from django.views.generic import ListView, DetailView

from apps.work_gallery.models import Work, Category
from apps.work_gallery.utils.mixins import CategoriesMixin
from utils.breadcrumbs.types import Breadcrumb
from utils.breadcrumbs.utils import reverse_bc
from utils.mixins import PageSettingsMixin


class WorkGalleryView(ListView, CategoriesMixin, PageSettingsMixin):
    template_name = 'work_gallery/works.html'
    queryset = Work.objects.filter(active=True)
    context_object_name = 'works'

    categories_queryset = Category.objects.exclude(work=None)

    viewname = 'work_gallery:list'


class SingleWorkView(DetailView, PageSettingsMixin):
    template_name = 'work_gallery/work.html'
    queryset = Work.objects.filter(active=True)
    slug_field = 'url'
    slug_url_kwarg = 'work_url'
    context_object_name = 'work'

    viewname = 'work_gallery:single'
    initial_breadcrumbs = [reverse_bc(view=WorkGalleryView)]

    def get_current_breadcrumb(self):
        return [Breadcrumb(self.object.title, '#')]

    def get_ceo_context(self) -> Dict[str, Any]:
        context = super().get_ceo_context()
        context.update({'work': self.object.title})
        return context
