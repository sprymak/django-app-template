from django import forms
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from unidecode import unidecode

from . import models


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = 'title', 'category'

    def clean(self):
        index = 2
        slug = self.cleaned_data['slug']
        if not slug:
            slug = slugify(unidecode(self.cleaned_data.get('title', '')))
        original_slug = slug
        while not slug or self._meta.model.objects.filter(slug=slug):
            slug = '%s-%d' % (original_slug, index)
            index += 1
        self.cleaned_data['slug'] = slug
        return super(ArticleForm, self).clean()
