from typing import Any, Dict, List

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from apps.news.forms import CommentForm
from apps.news.models import Article, Like
from apps.news.utils.mixins import LatestArticlesMixin, CommentsMixin
from utils.breadcrumbs.types import Breadcrumb
from utils.breadcrumbs.utils import reverse_bc
from utils.mixins import PageSettingsMixin


# class ArticleListView(ListView, LatestArticlesMixin, PageSettingsMixin):
#     template_name = 'promotions/promotions.html'
#     page_title = 'Блог'
#
#     queryset = Article.objects.filter(status='published')


class ArticleView(DetailView, FormView, PageSettingsMixin, LatestArticlesMixin, CommentsMixin):
    model = Article
    slug_field = 'url'
    slug_url_kwarg = 'article_url'
    context_object_name = 'article'
    template_name = 'news/article.html'
    max_articles = 3
    max_comments = 10

    def get_context_data(self, **kwargs):
        return super().get_context_data(liked=Like.objects.filter(article=self.get_object(), session_id=self.request.session.session_key).exists(), **kwargs)

    # #### PageSettingsMixin ####

    viewname = 'news:article'
    initial_breadcrumbs = [reverse_bc(viewname='tags:all')]

    def get_current_breadcrumb(self) -> List[Breadcrumb]:
        return [Breadcrumb(self.object.title, reverse_lazy('news:article', args=(self.object.url,)))]

    def get_ceo_context(self) -> Dict[str, Any]:
        return {'article': self.object.title}

    # #### FormMixin (FormView) ####

    form_class = CommentForm

    def get_success_url(self):
        url = reverse_lazy('news:article', kwargs={'article_url': self.get_object().url})
        return f'{url}#{self.comment.tag_id()}' if self.comment else url

    def get_initial(self):
        return {'article': self.get_object().id}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):  # Slip author object into data dict
            data = kwargs['data'].copy()
            data['author'] = self.request.user.id
            kwargs['data'] = data
        return kwargs

    def form_valid(self, form):
        self.comment = form.save()
        return super().form_valid(form)

    # FormView
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


def like_view(request, article_url):
    article = Article.objects.filter(url=article_url, status='published').first()
    if article is None:
        raise Http404('Статья не найдена')

    like = Like.objects.filter(article=article, session_id=request.session.session_key)

    if like.exists():
        like.delete()
        liked = False
    else:
        Like.objects.create(article=article, session_id=request.session.session_key)
        liked = True

    return HttpResponse(render_to_string('news/chunks/ajax/likes.html', {'liked': liked, 'overall': article.like_set.count()}), status=200)
