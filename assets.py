from django_assets import Bundle, register


register('{{ app_name }}_css', Bundle(
    Bundle(
        "{{ app_name }}/styles/{{ app_name }}.scss",
        filters="pyscss",
    ),
    filters='cssrewrite,cssmin',
    output='_/{{ app_name }}.css'
))

register('{{ app_name }}_js', Bundle(
    Bundle(
        "{{ app_name }}/scripts/{{ app_name }}.coffee",
        filters='coffeescript,jsmin',
    ),
    Bundle(
        "{{ app_name }}/scripts/{{ app_name }}.js",
        filters='jsmin'
    ),
    output='_/{{ app_name }}.js'
))
