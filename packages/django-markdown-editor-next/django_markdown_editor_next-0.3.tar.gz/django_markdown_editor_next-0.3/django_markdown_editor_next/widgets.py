# django_markdown_editor_next/widgets.py

from django import forms
from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe
from django.conf import settings

class MarkdownEditorWidget(Textarea):
    template_name = 'django_markdown_editor_next/widget.html'

    def __init__(self, *args, **kwargs):
        self.custom_toolbar = kwargs.pop('custom_toolbar', None)
        super().__init__(*args, **kwargs)
        self.attrs['class'] = 'markdown-editor'

    class Media:
        css = {
            'all': ('django_markdown_editor_next/css/markdown_editor.css',)
        }
        js = (
            'django_markdown_editor_next/js/markdown_editor.js',
            'https://cdnjs.cloudflare.com/ajax/libs/marked/2.0.3/marked.min.js',
        )

    def render(self, name, value, attrs=None, renderer=None):
        if renderer is None:
            renderer = forms.renderers.get_default_renderer()
        context = self.get_context(name, value, attrs)
        context['widget']['custom_toolbar'] = self.custom_toolbar
        return mark_safe(renderer.render(self.template_name, context))