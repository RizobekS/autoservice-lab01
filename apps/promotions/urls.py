from django.urls import path, register_converter

from apps.promotions.utils.urlconverters import CategoryUrlFilter
from apps.promotions.views import PromotionView, PromotionListView, PromotionCategoryView

app_name = 'promotions'

register_converter(CategoryUrlFilter, 'ctg_filter')

urlpatterns = [
    path('', PromotionListView.as_view(), name='list'),
    path('<ctg_filter:category_url>/', PromotionCategoryView.as_view(), name='category'),
    path('<str:promotion_url>/', PromotionView.as_view(), name='promotion')
]
