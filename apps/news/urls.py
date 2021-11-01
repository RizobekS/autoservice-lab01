from django.urls import path

from .views import like_view, NewsArticleView, ArticleListView

app_name = 'news'

urlpatterns = [
    path('', ArticleListView.as_view(), name='list'),
    path('<str:article_url>/', NewsArticleView.as_view(), name='article'),
    # path for like is already exists in knowledge base, so it is not duplicated
]
