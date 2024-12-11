# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'funkyheatmappy'
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
html_logo = 'https://raw.githubusercontent.com/funkyheatmap/logo/refs/heads/main/src/funkyheatmap_edited.svg'
html_sidebars = {
    '**': [
        'about.html',
        'links.html',
        'implementations.html',
        'examples.html',
        'navigation.html',
    ]
}

html_theme_options = {
    "github_user": "funkyheatmap",
    "github_repo": "funkyheatmappy",
    "fixed_sidebar": True,
    "github_banner": True,
    "github_button": False,
    "logo": "https://raw.githubusercontent.com/funkyheatmap/logo/refs/heads/main/src/funkyheatmap_edited.svg",
}
