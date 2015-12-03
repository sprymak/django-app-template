from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from . import forms
from . import models
from . import search


ITEMS_PER_PAGE = getattr(settings, "{{ app_name|upper }}_ITEMS_PER_PAGE", 25)

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

    page_number = request.GET.get('page')
    paginator = Paginator(object_filter.qs, ITEMS_PER_PAGE)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)

    return render(request, template_name, {
        'filter': object_filter.qs,
        'object_list': page.object_list,
        'page_obj': page,
        'paginator': paginator,
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
