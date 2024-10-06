
# Configuration file for the Sphinx documentation builder.

project = 'test_project'
copyright = '2024, Test Author'
author = 'Test Author'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_static_path = ['_static']
