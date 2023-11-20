from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('articles/exchange/<int:article_pk1>/<int:article_pk2>/<int:article_much1>/', views.exchange),
]
