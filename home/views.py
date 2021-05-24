from django.shortcuts import render
from django.views.generic import TemplateView
from articles.models import Article
from accounts.forms import ProfileForm


class HomePageView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured = Article.get_random()
        context["articles"] = Article.objects.all()[:5]
        context["featured"] = featured
        if self.request.user.is_authenticated:
            context["profile"] = self.request.user.profile
            form = ProfileForm()
            context["form"] = form
            print(context["profile"])
        return context
