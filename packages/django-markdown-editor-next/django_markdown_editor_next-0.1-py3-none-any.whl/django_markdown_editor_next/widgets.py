# django_markdown_editor/widgets.py
from django import forms
from django.forms.widgets import Textarea

class MarkdownEditorWidget(Textarea):
    template_name = 'django_markdown_editor/widget.html'

    class Media:
        css = {
            'all': ('django_markdown_editor/css/markdown_editor.css',)
        }
        js = ('django_markdown_editor/js/markdown_editor.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['class'] = 'markdown-editor'