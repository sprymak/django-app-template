import django.template


custom_builtins = [
    'utils.django.templatetags.collections_utils',
    'utils.django.templatetags.form_utils',
    'utils.django.templatetags.http_utils',
]

# Add our own template tags library to the builtins.
library_name = __name__.rsplit('.', 1)[0] + '.templatetags'
if not library_name in django.template.libraries:
    custom_builtins.insert(0, library_name)

for library_name in custom_builtins:
    if not library_name in django.template.builtins:
        django.template.add_to_builtins(library_name)
