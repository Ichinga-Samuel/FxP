from django.contrib import admin
from .models import Article, Course


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'status', 'banner')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'content', 'course')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


admin.site.register(Course)
