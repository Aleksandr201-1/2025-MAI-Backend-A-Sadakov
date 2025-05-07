from django.urls import path
from .views import (
    search_profile_view, list_profiles_view, create_profile_view,
    search_category_view, list_categories_view, create_category_view,
    search_goods_view, list_goods_view, create_goods_view,
    search_purchase_view, list_purchase_view, create_purchase_view,
)

urlpatterns = [
    # Profile endpoints
    path('profile/search/', search_profile_view, name='search_profile'),
    path('profile/', list_profiles_view, name='list_profiles'),
    path('profile/create/', create_profile_view, name='create_profile'),

    # Category endpoints
    path('category/search/', search_category_view, name='search_category'),
    path('category/', list_categories_view, name='list_categories'),
    path('category/create/', create_category_view, name='create_category'),

    # Goods endpoints
    path('goods/search/', search_goods_view, name='search_goods'),
    path('goods/', list_goods_view, name='list_goods'),
    path('goods/create/', create_goods_view, name='create_goods'),

    # Purchase endpoints
    path('purchase/search/', search_purchase_view, name='search_purchase'),
    path('purchase/', list_purchase_view, name='list_purchase'),
    path('purchase/create/', create_purchase_view, name='create_purchase'),
]
