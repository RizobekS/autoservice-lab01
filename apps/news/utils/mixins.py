from typing import Any, Dict, List

from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin

from apps.news.models import Article, Comment


class LatestArticlesMixin(ContextMixin):
    """
        Adds news to your context, ordered by time in ascending manner
        Tries to exclude current record if object variable is found

        max_articles: int - Number of Articles to retrieve, 10 by default
        context_name_articles: str - name of article list variable in context
    """
    max_articles: int = 10
    context_name_articles: str = 'latest_articles'

    def get_latest_articles(self) -> List[Article]:
        if hasattr(self, 'object'):
            obj = getattr(self, 'object')
            articles = Article.objects.filter(status='published').exclude(id=obj.id)
        else:
            articles = Article.objects.filter(status='published')
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
