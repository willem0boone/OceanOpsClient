import importlib.util
import sys
from pathlib import Path
# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'OceanOpsClient'
copyright = '2026, Willem Boone'
author = 'Willem Boone'


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

_VERSION_PATH = ROOT / "OceanOpsClient" / "_version.py"
_VERSION_SPEC = importlib.util.spec_from_file_location("OceanOpsClient._version", _VERSION_PATH)
assert _VERSION_SPEC and _VERSION_SPEC.loader
_VERSION_MODULE = importlib.util.module_from_spec(_VERSION_SPEC)
_VERSION_SPEC.loader.exec_module(_VERSION_MODULE)

version = _VERSION_MODULE.get_version()
release = version


# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output
html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

html_context = {
    "display_github": True, # Integrate GitHub
    "github_user": "willem0boone", # Username
    "github_repo": "template_RTD", # Repo name
    "github_version": "master", # Version
    "conf_py_path": "/docs/source/", # Path in the checkout to the docs root
}