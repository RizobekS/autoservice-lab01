from random import randint
from typing import Any, Dict, List

from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from apps.news.forms import CommentForm
from apps.news.models import Article, Like
from apps.news.utils.mixins import LatestArticlesMixin, CommentsMixin
from apps.promotions.models import Promotion
from utils.breadcrumbs.types import Breadcrumb
from utils.breadcrumbs.utils import reverse_bc
from utils.mixins import PageSettingsMixin

# Base view for Articles at news page and knowledge_base
from utils.opengraph import OpengraphMixin
from utils.opengraph.utils import og_thumbnail


class BaseArticleView(DetailView, FormView, PageSettingsMixin, LatestArticlesMixin, CommentsMixin, OpengraphMixin):
    template_name = 'news/article.html'
    slug_field = 'url'
    slug_url_kwarg = 'article_url'
    context_object_name = 'article'
    max_articles = 3
    max_comments = 10

    def get_og_tags(self, **kwargs) -> dict:
        meta_context = super().as_context()

        kwargs.update({
            'og:title': meta_context['page_title'],
            'og:description': meta_context['meta_description'],
            **og_thumbnail(self.request, self.object, 'icon_thumbnail'),
            'og:url': self.request.build_absolute_uri(self.request.path),
        })
        return super().get_og_tags(**kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'liked': Like.objects.filter(article=self.get_object(), session_id=self.request.session.session_key).exists()
        })
        return super().get_context_data(**kwargs)

    # #### PageSettingsMixin ####

    def get_ceo_context(self, **kwargs) -> Dict[str, Any]:
        kwargs.update({'article': self.object.title, 'short_description': self.object.short_description})
        return super().get_ceo_context(**kwargs)

    # #### FormMixin (FormView) ####

    form_class = CommentForm

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


# Displayed in knowledge_base
class KnowledgeBaseArticleView(BaseArticleView):
    queryset = Article.objects.filter(is_news=False)  # Check only among knowledge_base articles
    latest_articles_queryset = Article.objects.filter(is_news=False)  # Retrieve only knowledge_base articles

    viewname = 'knowledge_base:article'
    initial_breadcrumbs = [reverse_bc(viewname='knowledge_base:list')]

    def get_object(self, queryset=None):
        """
            Creates navigation by h4 headers throughout the article content:
                Adds 'navigation' attribute to object, containing {<header id>: <header text>} dictionary
                Adds html id attribute to all h4s in the text
        """
        if getattr(self, 'object', None):  # Do not bother recreating self.object attribute if it already exists
            return self.object
        else:
            obj = super().get_object(queryset)

            soup = BeautifulSoup(obj.text, "html.parser")
            navigation = {}
            h4s = soup.find_all('h4')
            for n, h4 in enumerate(h4s):
                html_id = f'header_h4-{n}'
                navigation[html_id] = h4.text
                h4['id'] = html_id
            obj.text = str(soup)
            obj.navigation = navigation

            return obj

    def get_context_data(self, **kwargs):
        kwargs['promotions'] = self.get_promotions()
        return super().get_context_data(**kwargs)

    def get_current_breadcrumb(self) -> List[Breadcrumb]:
        return [Breadcrumb(self.object.title, reverse_lazy('knowledge_base:article', args=(self.object.url,)))]

    def get_success_url(self):
        url = reverse_lazy('knowledge_base:article', kwargs={'article_url': self.get_object().url})
        return f'{url}#{self.comment.tag_id()}' if self.comment else url

    def get_promotions(self):
        """ Get related promotions (each promotion can be related to a knowledge base article). If no related promotions - select 3 arbitrary ones """
        promotions = self.object.promotion_set.filter(active=True)
        if promotions.exists():
            promotions = promotions[:3]
        else:
            # Get random promotion entries
            queryset = Promotion.objects.filter(active=True)
            promotions = []
            count = queryset.count()
            min_count = min(3, count)  # In case if there are less than 3 Promotions
            while len(promotions) < min_count:
                rand = randint(0, count - 1)
                item = queryset[rand]
                if item not in promotions:
                    promotions.append(item)
        return promotions


# Displayed at news page
class NewsArticleView(BaseArticleView):
    queryset = Article.objects.filter(is_news=True)  # Exclude articles from knowledge_base
    latest_articles_queryset = Article.objects.filter(is_news=True)  # Retrieve only news articles

    viewname = 'news:article'
    initial_breadcrumbs = [reverse_bc(viewname='news:list')]

    def get_current_breadcrumb(self) -> List[Breadcrumb]:
        return [Breadcrumb(self.object.title, reverse_lazy('news:article', args=(self.object.url,)))]

    def get_success_url(self):
        url = reverse_lazy('news:article', kwargs={'article_url': self.get_object().url})
        return f'{url}#{self.comment.tag_id()}' if self.comment else url


# News list page
class ArticleListView(ListView, PageSettingsMixin):
    template_name = 'news/news.html'
    ordering = '-date'
    context_object_name = 'news'
    queryset = Article.objects.filter(status='published', is_news=True)

    viewname = 'news:list'


def like_view(request, article_url):
    if request.is_ajax():
        article = Article.objects.filter(url=article_url, status='published').first()
        if article is None:
            raise Http404('Статья/Новость не найдена')

        like = Like.objects.filter(article=article, session_id=request.session.session_key)

        if like.exists():
            like.delete()
            liked = False
        else:
            Like.objects.create(article=article, session_id=request.session.session_key)
            liked = True

        return HttpResponse(render_to_string('news/chunks/ajax/likes.html', {'liked': liked, 'overall': article.like_set.count()}), status=200)
    else:
        raise Http404()
