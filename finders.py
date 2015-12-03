from django.contrib.staticfiles import finders as static_finders


class {{ app_name|title }}AssetsFinder(static_finders.AppDirectoriesFinder):
    source_dir = 'assets'
