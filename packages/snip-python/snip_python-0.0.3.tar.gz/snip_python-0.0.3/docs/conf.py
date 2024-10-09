# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Snip Python"
copyright = "2024, Sebastian B. Mohr"
author = "Sebastian B. Mohr"

master_doc = "index"
language = "en"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


templates_path = ["_templates"]
exclude_patterns = []


extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
    "sphinxcontrib.typer",
    "sphinx.ext.napoleon",
    # "myst_parser",
    "myst_nb",
]
autosummary_generate = True  # Turn on sphinx.ext.autosummary
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "jsonschema": ("https://python-jsonschema.readthedocs.io/en/stable", None),
}
nb_execution_mode = "off"
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_theme_options = {
    "light_logo": "favicon-128x128-light.png",
    "dark_logo": "favicon-128x128-dark.png",
    "light_css_variables": {
        "color-brand-primary": "#2f3992",
        "color-brand-content": "#dee2e6",
    },
    "dark_css_variables": {
        "color-brand-primary": "#2f3992",
        "color-brand-content": "#dee2e6",
    },
}
html_css_files = [
    "custom.css",
]
