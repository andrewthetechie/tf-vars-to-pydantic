"""Sphinx configuration."""
project = "Tf Vars To Pydantic"
author = "Andrew Herrington"
copyright = "2023, Andrew Herrington"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
