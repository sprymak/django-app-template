from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from . import forms
from . import models
from . import search


SUCCESS_MESSAGES = {
    'add_article': _('Article <strong>%(title)s</strong> successfully created.'),
    'change_article': _('Article <strong>%(title)s</strong> successfully changed.'),
    'delete_article': _('Article <strong>%(title)s</strong> successfully deleted.'),
}


class ArticleDetail(generic.DetailView):
    model = models.Article


article_detail = ArticleDetail.as_view()


def article_list(request, template_name='{{ app_name }}/article_list.html'):
    object_list = models.Article.objects.public()
    object_filter = search.ArticleFilter(request.GET, queryset=object_list)
    return render(request, template_name, {
        'object_list': object_list,
        'filter': object_filter,
    })


@login_required
@permission_required('{{ app_name }}.add_article')
def add_article(
        request, form_class=forms.ArticleForm, extra_context=None,
        template_name='{{ app_name }}/article_form.html'):
    context_dict = extra_context or {}
    form = form_class(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        messages.success(
            request, SUCCESS_MESSAGES['add_article'] % form.cleaned_data)
        return redirect('{{ app_name }}-article-detail', form.instance.pk)
    context_dict.update(form=form)
    return render(request, template_name, context_dict)


@login_required
@permission_required('{{ app_name }}.change_article')
def change_article(
        request, slug, form_class=forms.ArticleForm, extra_context=None,
        template_name='{{ app_name }}/article_form.html'):
    context_dict = extra_context or {}
    obj = get_object_or_404(models.Article.objects.all(), slug=slug)
    if obj.author != request.user:
        return HttpResponseForbidden()

    form = form_class(
        request.POST or None, files=request.FILES or None, instance=obj)
    if form.is_valid():
        form.instance.updated_by = request.user
        form.save()
        messages.success(
            request, SUCCESS_MESSAGES['change_article'] % form.cleaned_data)
        return redirect(request.GET.get(REDIRECT_FIELD_NAME, reverse(
            '{{ app_name }}-article-detail', args=[slug])))
    context_dict.update(form=form, object=obj, cut_marker='<!--more-->')
    return render(request, template_name, context_dict)


@login_required
@permission_required('{{ app_name }}.delete_article')
def delete_article(
        request, pk, extra_context=None,
        template_name='{{ app_name }}/article_confirm_delete'):
    obj = get_object_or_404(models.Article.objects.all(), pk=pk)
    if obj.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        obj.delete()
        messages.success(
            request, SUCCESS_MESSAGES['delete_article'] % obj.__dict__)
        return redirect(request.GET.get(REDIRECT_FIELD_NAME, reverse(
            '{{ app_name }}-article-list')))

    context_dict = extra_context or {}
    context_dict.update(object=obj)
    return render(request, template_name, context_dict)
