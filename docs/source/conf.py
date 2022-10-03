# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/main/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
from datetime import date

# import sys
# sys.path.insert(0, os.path.abspath('../../'))

# -- Project information -----------------------------------------------------

project = "Arsenal"
copyright = f"{date.today().year}, ATLAS"
author = (
    "Marissa Dotter, Keith Manville, Colin Busho*, Aidan Fennelly"
)

# The full version, including alpha/beta/rc tags
if os.environ.get("CI_COMMIT_TAG"):
    release = os.environ["CI_COMMIT_TAG"]
else:
    release = "latest"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "autoapi.extension",
    "myst_parser",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "PIL": ("https://pillow.readthedocs.io/en/stable/", None)
}
tls_verify = False

# Autodoc settings
autodoc_typehints = "description"

# Autoapi settings
autoapi_options = ["members", "undoc-members", "show-inheritance", "show-module-summary"]
autoapi_python_class_content = "both"
autoapi_type = "python"
autoapi_dirs = ["../../arsenal/"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["**/_tests"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"
html_logo = "../assets/arsenal_logo.png"
html_theme_options = {
    "logo_only": False,
    "display_version": True,
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# favicon location
# html_favicon = "../assets/icons/favicon.ico"
