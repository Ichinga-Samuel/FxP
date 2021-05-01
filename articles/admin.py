from django.contrib import admin
from django.contrib.auth.models import User

from .models import Article, Course, Tags


class ArticleInline(admin.TabularInline):
    model = User


class ArticleFilter(admin.SimpleListFilter):
    title = 'Duration'
    parameter_name = 'duration'

    def lookups(self, request, model_admin):
        return ('short', 'Short'), ('average', 'Average'), ('long', 'Long'),

    def queryset(self, request, queryset):
        if self.value() == 'short':
            return queryset.filter(duration__lte=20)

        elif self.value() == 'average':
            return queryset.filter(duration__gt=20, duration__lte=40)

        elif self.value() == 'long':
            return queryset.filter(duration__gt=40)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # inlines = [ArticleInline]
    save_on_top = True
    view_on_site = True
    list_select_related = ('author', 'course')
    fieldsets = (('Main', {'fields': ('title', 'status', 'banner', 'summary', 'num', 'slug', 'content', 'author', 'course', 'tags')}),
                 ('Time', {'fields': ('publish', 'duration', 'created'), 'classes': ('collapse', 'wide')}))
    readonly_fields = ('created',)
    list_display = ('title', 'publish', 'status', 'author', 'duration', 'summary')
    list_display_links = ('summary', )
    list_editable = ('status', 'duration', 'title')
    empty_value_display = 'UNSET'
    list_filter = ('status', 'publish', 'author', 'tags', ArticleFilter,)
    search_fields = ('title', 'content', 'course', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author', 'tags')
    date_hierarchy = 'publish'
    ordering = ('status', 'num', 'publish')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    view_on_site = True
    list_display = ('name', 'level')
    list_display_links = None
    list_editable = ('name', 'level')
    search_fields = ('name', 'tags', 'level')
    list_filter = ('tags', 'name', 'level')
    raw_id_fields = ('tags',)


admin.site.register(Tags)
