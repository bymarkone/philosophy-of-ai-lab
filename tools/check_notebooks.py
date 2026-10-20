"""Execute every notebook under labs/ top to bottom. Fails on the first error."""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
paths = sorted(root.glob("labs/**/*.ipynb"))
if len(sys.argv) > 1:
    paths = [p for p in paths if any(a in str(p) for a in sys.argv[1:])]
for path in paths:
    nb = nbformat.read(path, as_version=4)
    NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}}).execute()
    errors = [o for c in nb.cells if c.cell_type == "code" for o in c.get("outputs", []) if o.output_type == "error"]
    print(f"{'FAIL' if errors else 'ok  '} {path.relative_to(root)}")
    if errors:
        sys.exit(1)
