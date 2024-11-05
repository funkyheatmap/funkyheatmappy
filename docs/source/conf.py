# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'funky\nheatmappy'
copyright = '2024, Artuur Couckuyt, Louise Deconinck'
author = 'Artuur Couckuyt, Louise Deconinck'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['autoapi.extension']
autoapi_dirs = ['../../funkyheatmappy']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_logo = 'https://raw.githubusercontent.com/funkyheatmap/logo/refs/heads/main/src/attempt1/funkyheatmap_edited.svg'
