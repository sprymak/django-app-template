from django.contrib import admin
from . import models


class ArticleAdmin(admin.ModelAdmin):
   list_display = (
        'title', 'is_private', 'date_created', 'date_updated', 'pk')
   search_fields = 'title',


admin.site.register(models.Article, ArticleAdmin)
