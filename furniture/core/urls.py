from django.urls import path
from .views import (
    profile_view,
    goods_list_view,
    categories_list_view
)
urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('goods/', goods_list_view, name='goods'),
    path('categories/', categories_list_view, name='categories'),
]
