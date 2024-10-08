# Django Markdown Editor

A Django package to support Markdown text editor in Django admin.

## Installation

```
pip install django-markdown-editor-next
```

## Usage

1. Add 'django_markdown_editor' to your INSTALLED_APPS setting.

2. In your models, use the MarkdownField:

```python
from django_markdown_editor.fields import MarkdownField

class MyModel(models.Model):
    content = MarkdownField()
```

3. That's it! The Django admin will now use the Markdown editor for this field.
## License

This project is licensed under the MIT License - see the LICENSE file for details.