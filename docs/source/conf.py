# Configuration file for the Sphinx documentation builder.

import nautilus_namecodes

# -- Project information -----------------------------------------------------

project: str = "nautilus-namecodes"
copyright: str = "2021, Nautilus Cyberneering GmbH "
author: str = "Cameron Garnham"

# The full version, including alpha/beta/rc tags
release: str = str(nautilus_namecodes.__version__)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions: list[str] = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.intersphinx"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: list[str] = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme: str = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path: list[str] = ["_static"]
