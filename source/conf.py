# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'End-to-End Machine Learning Pipeline for Distance Estimation and Human-Robot Interaction in Autonomous Systems'
copyright = '2025, MD ASLAM ANSARI'
author = 'MD ASLAM ANSARI'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_rtd_theme',
]

pygments_style = "friendly"  # Or try: 'colorful', 'monokai', 'paraiso-light', etc.

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
html_css_files = ['custom.css']
