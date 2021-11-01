from django.urls import path

from apps.knowledge_base.views import AnsweredQuestionView, SymptomView, KnowledgeBaseView
from apps.news.views import like_view, KnowledgeBaseArticleView

app_name = 'knowledge_base'

urlpatterns = [
    path('knowledge-base/', KnowledgeBaseView.as_view(), name='list'),
    path('knowledge-base/faq/<str:url>/', AnsweredQuestionView.as_view(), name='answered-question'),
    path('knowledge-base/symptom/<str:url>/', SymptomView.as_view(), name='symptom'),
    path('blog/<str:article_url>/', KnowledgeBaseArticleView.as_view(), name='article'),
    path('blog/like/<str:article_url>/', like_view, name='like'),
]
