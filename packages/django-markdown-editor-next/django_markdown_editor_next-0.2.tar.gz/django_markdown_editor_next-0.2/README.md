# Django Markdown Editor

A feature-rich Markdown editor for Django admin with real-time preview, image uploads, and customizable toolbar.

## Installation

```bash
pip install django-markdown-editor
```

## Setup

1. Add 'django_markdown_editor' to your INSTALLED_APPS setting.

2. Add the following to your project's urls.py:

   ```python
   from django.urls import path, include

   urlpatterns = [
       # ... your other url patterns
       path('markdown-editor/', include('django_markdown_editor.urls')),
   ]
   ```

3. Ensure your `MEDIA_ROOT` and `MEDIA_URL` settings are configured in your Django settings:

   ```python
   MEDIA_ROOT = BASE_DIR / 'media'
   MEDIA_URL = '/media/'
   ```

4. In your models, use the MarkdownField:

   ```python
   from django_markdown_editor.fields import MarkdownField

   class MyModel(models.Model):
       content = MarkdownField()
   ```

## Features

- Real-time Markdown preview
- Image uploads
- Customizable toolbar
- Keyboard shortcuts

## Customizing the Toolbar

You can customize the toolbar buttons when defining your model field:

```python
content = MarkdownField(
    custom_toolbar=[
        {'action': 'bold', 'icon': 'fas fa-bold', 'title': 'Bold'},
        {'action': 'italic', 'icon': 'fas fa-italic', 'title': 'Italic'},
        {'action': 'link', 'icon': 'fas fa-link', 'title': 'Link'},
        {'action': 'image', 'icon': 'fas fa-image', 'title': 'Image'},
        {'action': 'preview', 'icon': 'fas fa-eye', 'title': 'Toggle Preview'}
    ]
)
```

## Keyboard Shortcuts

- Ctrl/Cmd + B: Bold
- Ctrl/Cmd + I: Italic
- Ctrl/Cmd + K: Insert Link

## License

This project is licensed under the MIT License - see the LICENSE file for details.