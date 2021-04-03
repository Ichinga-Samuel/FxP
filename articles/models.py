from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField
from random import randint

F = models.F


class Article(models.Model):
    SC = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=250)
    course = models.ManyToManyField('Course')
    num = models.IntegerField(help_text='use this to arrange the lessons serially for each level')
    banner = models.ImageField(upload_to=f'uploads/articles/images/')
    status = models.CharField(max_length=10, choices=SC, default='draft', help_text='If the lesson is ready. Set the '
                                                                                    'status to publish')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, related_name='Articles')
    content = HTMLField()
    summary = models.TextField(max_length=500, help_text='brief summary of the lesson')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=250, help_text="separate tags with commas eg 'crypto, socks, forex' ")
    duration = models.DurationField(null=True, default=20)

    class Meta:
        ordering = ['num', '-publish', ]

    def __str__(self):
        return f"{self.course.name}{self.title}"

    def get_name(self):
        return str(self)

    def get_absolute_url(self):
        return reverse('articles:articles_detail', args=[self.pk])

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
    content = HTMLField()

    class Meta:
        ordering = ['level', 'name', ]


# def next_url(self):
#     m = self.__class__                             # the article class
#     n = self.num + 1                               # the lesson Number
#     a = m.objects.filter(num__exact=n, status='published').first()
#     return m.get_absolute_url(a)
#
# def prev_url(self):
#     m = self.__class__                             # the article class
#     n = self.num - 1                               # the lesson Number
#     a = m.objects.filter(num__exact=n).first()
#     return a.get_absolute_url()
