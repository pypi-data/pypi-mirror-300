# setup.py
from setuptools import setup, find_packages

setup(
    name='django-markdown-editor-next',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A Django package to support Markdown text editor in Django admin',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/aliahadmd/django-markdown-editor-next',
    author='Ali',
    author_email='ali@aliahad.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=2.2',
    ],
)
