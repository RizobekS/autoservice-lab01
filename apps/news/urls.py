from django.urls import path

from .views import ArticleView, like_view

app_name = 'news'

urlpatterns = [
    # path('', ArticleListView.as_view(), name='list'),
    path('<str:article_url>/', ArticleView.as_view(), name='article'),
    path('like/<str:article_url>/', like_view, name='like')
    # path("", views.news_list_view, name="news"),
]
