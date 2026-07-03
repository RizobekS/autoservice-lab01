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
    template_name = 'work_gallery/new_works.html'
    queryset = Work.objects.prefetch_related('image_set', 'categories').filter(active=True).order_by('-id')
    context_object_name = 'works'
    paginate_by = 30

    categories_queryset = Category.objects.exclude(work=None).distinct()

    viewname = 'work_gallery:list'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.selected_category = self.request.GET.get('category', '')
        if self.selected_category:
            queryset = queryset.filter(categories__url=self.selected_category)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context.get('page_obj')
        total_count = context.get('paginator').count if context.get('paginator') else len(context['works'])
        shown_count = page_obj.end_index() if page_obj else len(context['works'])

        context.update({
            'selected_category': self.selected_category,
            'works_total_count': total_count,
            'works_shown_count': shown_count,
        })
        return context


class SingleWorkView(DetailView, PageSettingsMixin, OpengraphMixin):
    template_name = 'work_gallery/new_work.html'
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_ids = self.object.categories.values_list('id', flat=True)
        context['related_works'] = Work.objects.prefetch_related('image_set', 'categories').filter(
            active=True,
            categories__id__in=category_ids,
        ).exclude(id=self.object.id).distinct().order_by('-id')[:4]
        return context

    def get_ceo_context(self, **kwargs) -> Dict[str, Any]:
        kwargs.update({'work': self.object.title})
        return super().get_ceo_context(**kwargs)
