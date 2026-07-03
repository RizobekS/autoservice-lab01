from django.urls import path

from apps.knowledge_base.views import AnsweredQuestionView, FaqListView, SymptomListView, SymptomView, KnowledgeBaseView
from apps.news.views import BlogListView, like_view, KnowledgeBaseArticleView

app_name = 'knowledge_base'

urlpatterns = [
    path('knowledge-base/', KnowledgeBaseView.as_view(), name='list'),
    path('knowledge-base/faq/', FaqListView.as_view(), name='faq'),
    path('knowledge-base/symptom/', SymptomListView.as_view(), name='symptom-list'),
    path('knowledge-base/faq/<str:url>/', AnsweredQuestionView.as_view(), name='answered-question'),
    path('knowledge-base/symptom/<str:url>/', SymptomView.as_view(), name='symptom'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/<str:article_url>/', KnowledgeBaseArticleView.as_view(), name='article'),
    path('blog/like/<str:article_url>/', like_view, name='like'),
]
