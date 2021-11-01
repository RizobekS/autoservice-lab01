from django.urls import path

from .views import ArticleView, like_view

app_name = 'news'

urlpatterns = [
    # path('', ArticleListView.as_view(), name='list'),
    # path("", views.news_list_view, name="news"),
]
