from django.urls import path, include

from apps.knowledge_base.views import AnsweredQuestionView, SymptomView, KnowledgeBaseView

app_name = 'knowledge_base'

urlpatterns = [
    path('knowledge-base/', KnowledgeBaseView.as_view(), name='list'),
    path('knowledge-base/faq/<str:url>/', AnsweredQuestionView.as_view(), name='answered-question'),
    path('knowledge-base/symptom/<str:url>/', SymptomView.as_view(), name='symptom'),
    path('blog/', include('apps.news.urls', namespace='news')),
]
