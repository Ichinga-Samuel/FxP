import os

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from .models import Article
from .forms import PostForm
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


class ArticleListView(ListView):
    queryset = Article.objects.all()
    context_object_name = 'articles'
    template_name = 'all.html'


class ArticleDetailView(DetailView):

    context_object_name = 'article'
    template_name = 'articles/article_detail.html'

    def get_queryset(self):
        self.article = Article.objects.filter(pk=self.kwargs['pk'], status='published').first()
        return Article.objects.filter(course=self.article.course.name, status='published')

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        qs = self.get_queryset()
        context['others'] = qs              # Article.objects.filter(level=self.object.level)
        pos = self.object.num
        context["next"] = qs[pos] if 1 <= pos < len(qs) else False
        context["prev"] = qs[pos-2] if pos > 1 else False
        return context


class ArticleCreateView(CreateView):
    model = Article
    template_name = 'article_create.html'
    form_class = PostForm
    success_url = 'home:homepage'


# @csrf_exempt
# def upload_image(request):
#     if request.method == "POST":
#         file_obj = request.FILES['file']
#         file_name_suffix = file_obj.name.split(".")[-1]
#         if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
#             return JsonResponse({"message": "Wrong file format"})
#
#         upload_time = timezone.now()
#         path = os.path.join(
#             settings.MEDIA_ROOT,
#             'tinymce',
#             str(upload_time.year),
#             str(upload_time.month),
#             str(upload_time.day)
#         )
#         # If there is no such path, create
#         if not os.path.exists(path):
#             os.makedirs(path)
#
#         file_path = os.path.join(path, file_obj.name)
#
#         file_url = f'{settings.MEDIA_URL}tinymce/{upload_time.year}/{upload_time.month}/{upload_time.day}/{file_obj.name}'
#
#         if os.path.exists(file_path):
#             return JsonResponse({
#                 "message": "file already exist",
#                 'location': file_url
#             })
#
#         with open(file_path, 'wb+') as f:
#             for chunk in file_obj.chunks():
#                 f.write(chunk)
#
#         return JsonResponse({
#             'message': 'Image uploaded successfully',
#             'location': file_url
#         })
#     return JsonResponse({'detail': "Wrong request"})
