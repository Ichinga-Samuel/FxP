from django.urls import path
from . import views



app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='articles_list'),
    path('<int:pk>', views.ArticleDetailView.as_view(), name='articles_detail'),
    path('create', views.ArticleCreateView.as_view(), name='create'),
]

# path('image_upload/', views.upload_image, name='image_upload')
