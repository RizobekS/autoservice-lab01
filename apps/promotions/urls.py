from django.urls import path

from apps.promotions.views import PromotionView, PromotionListView, PromotionCategoryView

app_name = 'promotions'

urlpatterns = [
    path('', PromotionListView.as_view(), name='list'),
    path('category/<str:category_url>/', PromotionCategoryView.as_view(), name='category'),
    path('<str:promotion_url>/', PromotionView.as_view(), name='promotion')
]
