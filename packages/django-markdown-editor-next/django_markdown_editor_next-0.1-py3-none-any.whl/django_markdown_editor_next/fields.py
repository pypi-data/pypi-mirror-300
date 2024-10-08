# django_markdown_editor/fields.py
from django.db import models
from .widgets import MarkdownEditorWidget

class MarkdownField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {'widget': MarkdownEditorWidget}
        defaults.update(kwargs)
        return super().formfield(**defaults)