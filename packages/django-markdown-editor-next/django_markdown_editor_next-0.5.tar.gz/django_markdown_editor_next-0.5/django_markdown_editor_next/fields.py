# django_markdown_editor_next/fields.py
from django.db import models
from .widgets import MarkdownEditorWidget

class MarkdownField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.custom_toolbar = kwargs.pop('custom_toolbar', None)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'widget': MarkdownEditorWidget(custom_toolbar=self.custom_toolbar)}
        defaults.update(kwargs)
        return super().formfield(**defaults)