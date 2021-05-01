from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('', views.CourseListView.as_view(), name='home')
]
