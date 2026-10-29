"""Tiny helper to write notebooks from Python: md(...) and code(...) cells."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

REPO = "https://github.com/bymarkone/philosophy-of-ai-lab"
COLAB = "https://colab.research.google.com/github/bymarkone/philosophy-of-ai-lab/blob/main"
RAW = "https://raw.githubusercontent.com/bymarkone/philosophy-of-ai-lab/main"


def raw(path: str) -> str:
    """URL of a file in the repo as served by GitHub, for images in markdown cells."""
    return f"{RAW}/{path}"


def colab(path: str) -> str:
    """Colab URL that opens a notebook straight from the GitHub repo."""
    return f"{COLAB}/{path}"

SETUP = f'''# Run this cell first. It fetches the lab's code from GitHub (10 to 30 seconds).
import importlib, importlib.util, os, subprocess, sys
pip = [sys.executable, "-m", "pip", "install", "-q"]
on_colab = "google.colab" in sys.modules or "COLAB_RELEASE_TAG" in os.environ
if importlib.util.find_spec("seminarlab") is None:
    subprocess.run(pip + ["git+{REPO}"], check=True)                                   # the code and what it needs
elif on_colab:
    subprocess.run(pip + ["--force-reinstall", "--no-deps", "git+{REPO}"], check=True)  # make sure it is today's version
for name in [m for m in sys.modules if m.startswith("seminarlab")]:
    del sys.modules[name]                                                              # forget any older copy
importlib.invalidate_caches()
print("ready")'''


def md(text):
    return new_markdown_cell(text.strip("\n"))


def code(text):
    return new_code_cell(text.strip("\n"))


def setup():
    return code(SETUP)


def write(cells, path):
    nb = new_notebook(cells=cells)
    for i, cell in enumerate(nb.cells):  # stable ids, so a rebuild only changes what you edited
        cell.id = f"{Path(path).stem}-{i:02d}"
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.metadata["language_info"] = {"name": "python"}
    nbformat.write(nb, path)
    print("wrote", path)
