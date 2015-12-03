from __future__ import unicode_literals
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):
    display_name = models.CharField(blank=True, default='', max_length=150)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = 'display_name',

    def __str__(self):
        return self.name


class ArticleQuerySet(models.query.QuerySet):
    def private(self):
        return self.filter(is_private=True)

    def public(self):
        return self.filter(is_private=False)


class ArticleManager(models.Manager):
    def private(self):
        return self.get_queryset().filter(is_private=True)

    def public(self):
        return self.get_queryset().filter(is_private=False)

    def get_query_set(self):
        return ArticleQuerySet(self.model)


@python_2_unicode_compatible
class Article(models.Model):
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created'))
    date_updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name=_('updated'))
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles')
    is_private = models.BooleanField(default=True, verbose_name=_('private'))
    category = models.ForeignKey(
        Category, null=True, blank=True, related_name='articles',
        verbose_name=_('category'))

    objects = ArticleManager()

    class Meta:
        permissions = (
            # extend default ['add_*', 'change_*', 'delete_*'] permissions
            ('index_article', _('Can index article')),
            ('get_article', _('Can get article')),
        )
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = '-date_created',

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('{{ app_name }}-article-detail', args=[self.slug])
