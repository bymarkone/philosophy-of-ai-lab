"""Build the Lab 2 notebooks. Run from the repo root: .venv/bin/python -m tools.build_lab2"""

from pathlib import Path

from tools.lab2 import index, part_a, part_b, part_c, part_d, part_e
from tools.nb import write

OUT = Path(__file__).resolve().parents[1] / "labs" / "lab2"

NOTEBOOKS = {
    "00-index.ipynb": index.cells,
    "01-neurons-as-logic.ipynb": part_a.cells,
    "02-the-perceptron.ipynb": part_b.cells,
    "03-breaking-the-perceptron.ipynb": part_c.cells,
    "04-a-hidden-layer.ipynb": part_d.cells,
    "05-what-did-it-learn.ipynb": part_e.cells,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in NOTEBOOKS.items():
        write(build(), OUT / name)
