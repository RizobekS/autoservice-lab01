from typing import Any, Dict

from django.views.generic import ListView, DetailView

from apps.work_gallery.models import Work, Category
from apps.work_gallery.utils.mixins import CategoriesMixin
from utils.breadcrumbs.types import Breadcrumb
from utils.breadcrumbs.utils import reverse_bc
from utils.mixins import PageSettingsMixin
from utils.opengraph import OpengraphMixin
from utils.opengraph.utils import og_thumbnail


class WorkGalleryView(ListView, CategoriesMixin, PageSettingsMixin):
    template_name = 'work_gallery/works.html'
    queryset = Work.objects.filter(active=True)
    context_object_name = 'works'

    categories_queryset = Category.objects.exclude(work=None)

    viewname = 'work_gallery:list'


class SingleWorkView(DetailView, PageSettingsMixin, OpengraphMixin):
    template_name = 'work_gallery/work.html'
    queryset = Work.objects.filter(active=True)
    slug_field = 'url'
    slug_url_kwarg = 'work_url'
    context_object_name = 'work'

    viewname = 'work_gallery:single'
    initial_breadcrumbs = [reverse_bc(view=WorkGalleryView)]

    def get_og_tags(self, **kwargs) -> dict:
        meta_context = super().as_context()

        kwargs.update({
            'og:title': meta_context['page_title'],
            'og:description': meta_context['meta_description'],
            **og_thumbnail(self.request, self.object.image_set.first(), 'page_thumbnail'),
            'og:url': self.request.build_absolute_uri(self.request.path),
        })
        return super().get_og_tags(**kwargs)

    def get_current_breadcrumb(self):
        return [Breadcrumb(self.object.title, '#')]

    def get_ceo_context(self, **kwargs) -> Dict[str, Any]:
        kwargs.update({'work': self.object.title})
        return super().get_ceo_context(**kwargs)
