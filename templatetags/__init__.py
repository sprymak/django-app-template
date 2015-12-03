import django
import django.template

register = django.template.Library()


@register.simple_tag
def version():
    from application import __version__
    return __version__
