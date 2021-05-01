import os

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from .models import Article, Course
from .forms import PostForm
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


class ArticleListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'articles/all.html'


class ArticleDetailView(TemplateView):

    context_object_name = 'article'
    template_name = 'articles/article_detail.html'

    def get_queryset(self):
        self.article = get_object_or_404(Article, pk=self.kwargs['pk'])
        return Article.objects.filter(course__name=self.article.course.name, status='published')

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        qs = self.get_queryset()
        context['article'] = self.article
        context['others'] = qs
        context["next"] = self.article.next_url()
        context["prev"] = self.article.prev_url()
        return context


class CourseListView(ListView):

    template_name = 'course/course_home.html'
    model = Course
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    template_name = 'course/course_detail.html'
    model = Course
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        # c = context['course'] = get_object_or_404(Course, pk=self.kwargs['pk'])
        context['lessons'] = self.object.article_set.all()
        return context


