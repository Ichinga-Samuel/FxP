from django.shortcuts import render
from django.views.generic import TemplateView
from articles.models import Article


class HomePageView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured = Article.get_random()
        context["articles"] = Article.objects.all()[:5]
        context["featured"] = featured
        return context
