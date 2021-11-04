# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path


def add_path_if_missing(path_str: str):
    """Little function that adds a path to the python path if it is missing."""

    if any(path_str == sys_path for sys_path in sys.path):
        pass
    else:
        sys.path += [path_str]


path_this: Path = Path(__file__).parent
add_path_if_missing(str(path_this.absolute()))


import _helpers  # pylint: disable=wrong-import-position

path_root: Path = _helpers.get_path_to_project_root()
path_src: Path = path_root.joinpath("src")

add_path_if_missing(str(path_src.absolute()))


import nautilus_namecodes  # pylint: disable=wrong-import-position

# -- Project information -----------------------------------------------------

project: str = "nautilus-namecodes"
copyright: str = (  # pylint: disable=redefined-builtin
    "2021, Nautilus Cyberneering GmbH "
)
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
