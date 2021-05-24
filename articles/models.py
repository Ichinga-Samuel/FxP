from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField
from random import randint

from accounts.models import Profile

F = models.F
User = settings.AUTH_USER_MODEL


class Article(models.Model):
    SC = ('draft', 'Draft'), ('published', 'Published')
    title = models.CharField(max_length=250)
    course = models.ForeignKey('Course', on_delete=models.RESTRICT)
    num = models.IntegerField(help_text='use this to arrange the lessons serially for each level', unique=True)
    banner = models.ImageField(upload_to=f'uploads/articles/images/')
    status = models.CharField(max_length=10, choices=SC, default='published', help_text='If the lesson is ready. Set the status to publish')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Articles')
    content = HTMLField()
    summary = models.TextField(max_length=500, help_text='brief summary of the lesson')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tags')
    duration = models.IntegerField(null=True, default=20)

    class Meta:
        ordering = ['num', '-publish', ]
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return f"{self.title}"

    def get_name(self):
        return str(self)

    def get_absolute_url(self):
        return reverse('articles:articles_detail', kwargs={'pk': self.pk})

    def next_url(self):
        m = self.__class__                             # the article class
        n = self.num + 1                               # the lesson Number
        if n <= m.objects.count():
            a = m.objects.get(num=n)
            return m.get_absolute_url(a)
        return None

    def prev_url(self):
        m = self.__class__                             # the article class
        n = self.num - 1                               # the lesson Number
        if n:
            a = m.objects.get(num=n)
            return a.get_absolute_url()
        return None

    @classmethod
    def get_random(cls):
        o = cls.objects.filter(status='published')
        if o:
            i = randint(0, len(o)-1)
            return o[i]
        return None


class Course(models.Model):
    LV = [('bg', 'Beginner'), ('inter', 'Intermediate'), ('ad', 'Advanced'), ('ex', 'Expert')]
    name = models.CharField(max_length=250)
    level = models.CharField(max_length=250, choices=LV, default='bg')
    banner = models.ImageField(upload_to=f'uploads/courses/images/')
    content = HTMLField()
    tags = models.ManyToManyField('Tags')

    class Meta:
        ordering = ['level', 'name', ]
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):

        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'pk': self.pk})


class Tags(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return f'{self.name}'
