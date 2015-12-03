from django.db.models import Q
import django_filters
from . import models


class UserFilter(django_filters.Filter):
    def filter(self, qs, value):
        lookups = (
            '%s__first_name__icontains', '%s__last_name__icontains',
            '%s__username__icontains')
        if value:
            q = Q()
            for v in lookups:
                q |= Q(**{v % self.name: value})
            return qs.filter(q).distinct()
        return qs


class ArticleFilter(django_filters.FilterSet):
    author = UserFilter(name='author')

    class Meta:
        model = models.Article
        fields = 'author', 'category'
