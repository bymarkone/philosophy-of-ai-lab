"""Tiny helper to write notebooks from Python: md(...) and code(...) cells."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

REPO = "https://github.com/bymarkone/philosophy-of-ai-lab"
COLAB = "https://colab.research.google.com/github/bymarkone/philosophy-of-ai-lab/blob/main"


def colab(path: str) -> str:
    """Colab URL that opens a notebook straight from the GitHub repo."""
    return f"{COLAB}/{path}"

SETUP = f'''# Run this cell first. It fetches the lab's code from GitHub (a few seconds).
import importlib.util, subprocess, sys
if importlib.util.find_spec("seminarlab") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "git+{REPO}"], check=True)
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
