from typing import Any, Dict, List

from django.db.models import Q
from django.urls import reverse
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin

from apps.news.models import Article, Comment
from apps.knowledge_base.models import FaqEntry, Symptom
from apps.tags.models import Tag


class InfoMaterialsSidebarMixin(ContextMixin):
    info_material_type = None
    latest_info_materials_limit = 5

    def get_info_material_categories(self):
        categories = [
            {
                'key': 'news',
                'title': 'Новости',
                'url': reverse('news:list'),
                'count': Article.objects.filter(status='published', is_news=True).count(),
            },
            {
                'key': 'articles',
                'title': 'Статьи',
                'url': reverse('knowledge_base:blog'),
                'count': Article.objects.filter(status='published', is_news=False).count(),
            },
            {
                'key': 'faq',
                'title': 'Вопрос-ответ',
                'url': reverse('knowledge_base:faq'),
                'count': FaqEntry.objects.filter(answered=True).count(),
            },
            {
                'key': 'symptom',
                'title': 'Симптомы',
                'url': reverse('knowledge_base:symptom-list'),
                'count': Symptom.objects.filter(active=True).count(),
            },
        ]
        for category in categories:
            category['active'] = category['key'] == self.info_material_type
        return categories

    def get_latest_info_materials(self):
        records = [
            *Article.objects.filter(status='published'),
            *FaqEntry.objects.filter(answered=True),
            *Symptom.objects.filter(active=True),
        ]
        records.sort(key=lambda item: item.date.timestamp() if item.date else 0, reverse=True)
        return records[:self.latest_info_materials_limit]

    def get_info_material_tags(self):
        return Tag.objects.filter(
            Q(article__status='published') |
            Q(faqentry__answered=True) |
            Q(symptom__active=True)
        ).distinct()

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'info_material_categories': self.get_info_material_categories(),
            'latest_info_materials': self.get_latest_info_materials(),
            'info_material_tags': self.get_info_material_tags(),
        })
        return context


class LatestArticlesMixin(ContextMixin):
    """
        Adds news to your context, ordered by time in ascending manner
        Tries to exclude current record if object variable is found

        max_articles: int - Number of Articles to retrieve, 10 by default. If None - no constraints
        context_name_articles: str - name of article list variable in context
    """
    max_articles: int = 10
    context_name_articles: str = 'latest_articles'
    latest_articles_queryset = Article.objects

    def get_latest_articles(self) -> List[Article]:
        if hasattr(self, 'object'):
            obj = getattr(self, 'object')
            articles = self.latest_articles_queryset.filter(status='published').exclude(id=obj.id)
        else:
            articles = self.latest_articles_queryset.filter(status='published')
        return articles[:self.max_articles] if self.max_articles else list(articles)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context[self.context_name_articles] = self.get_latest_articles()
        return context


class CommentsMixin(SingleObjectMixin, ContextMixin):
    """
        Adds comment list to your context, which is ordered by time ascending.
        Uses self.object to retrieve current record's comments.
        Note: mixin retrieves only root comments (replies are not included),
        replies should be retrieved using RelatedManager.

        max_comments: int - Number of comments to retrieve, 30 by default
    """
    max_comments = 30

    def get_comments(self) -> List[Comment]:
        article = self.get_object()
        comments = Comment.objects.filter(article=article, visible=True, reply_to=None)
        return comments[:self.max_comments] if self.max_comments else list(comments)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_comments()
        return context
