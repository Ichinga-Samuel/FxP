from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='articles_list'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='articles_detail'),
]
