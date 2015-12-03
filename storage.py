from django.core.files.storage import FileSystemStorage


class {{ app_name|title }}Storage(FileSystemStorage):
    pass
