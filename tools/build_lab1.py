"""Build the Lab 1 notebooks. Run from the repo root: .venv/bin/python -m tools.build_lab1"""

from pathlib import Path

from tools.lab1 import index, part_a, part_b, part_c, part_d, part_e
from seminarlab.lab1.timeline import draw_timeline
from tools.nb import write

OUT = Path(__file__).resolve().parents[1] / "labs" / "lab1"

NOTEBOOKS = {
    "00-index.ipynb": index.cells,
    "01-how-big-is-the-game.ipynb": part_a.cells,
    "02-one-search-three-games.ipynb": part_b.cells,
    "03-recognising-a-letter.ipynb": part_c.cells,
    "04-planning-and-the-frame-problem.ipynb": part_d.cells,
    "05-turing-machine-and-automaton.ipynb": part_e.cells,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in NOTEBOOKS.items():
        write(build(), OUT / name)
    (OUT / "img").mkdir(exist_ok=True)
    draw_timeline(str(OUT / "img" / "timeline.png"))
    print("wrote", OUT / "img" / "timeline.png")
