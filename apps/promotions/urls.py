from django.urls import path

from apps.promotions.views import PromotionView, PromotionListView

app_name = 'promotions'

urlpatterns = [
    path('', PromotionListView.as_view(), name='list'),
    path('<str:promotion_url>/', PromotionView.as_view(), name='promotion')
]
