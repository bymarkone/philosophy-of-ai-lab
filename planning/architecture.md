# Architecture

## Vision

Five laboratories, one per seminar session from 2 to 6. Each lab is a set of short Jupyter notebooks that open in Google Colab from a link in the README. Students run the cells, read the prose, change one or two things, and see what happens. The prose carries the insight and quotes the day's papers. The code is short enough to read in full.

## Layout

```
seminar-laboratory/
  README.md              Colab links, one paragraph per lab
  pyproject.toml         package `seminarlab`, deps: numpy, matplotlib, python-chess
  seminarlab/
    lab1/                games, search, letters, planning, machines, plots
    lab2/ ...            one subpackage per lab
  labs/
    lab1/
      00-index.ipynb     what the lab is, how the afternoon runs
      01-...ipynb        one notebook per part
      INSTRUCTOR.md      timing, what to project, where students get stuck
  tests/                 pytest, one file per module
  tools/
    nb.py                md()/code() helpers and the Colab setup cell
    lab1/part_*.py       the notebooks' source: prose and code cells as Python
    build_lab1.py        writes labs/lab1/*.ipynb from tools/lab1
    check_notebooks.py   executes every notebook top to bottom
  planning/              this directory
```

## Decisions

- **Colab from GitHub.** Each notebook starts with one cell that installs the package from the GitHub repo. Nothing else to set up. The instructor can also run locally with the `.venv`.
- **Package plus notebooks.** Boring code (board rules, move generation, drawing) lives in `seminarlab` so the notebooks stay short. The code that carries the lesson (minimax, the Turing machine table, the perceptron update rule later) is written in the notebook itself, in full, so students read it.
- **numpy and matplotlib only** for labs 1 to 3, plus python-chess for chess rules in lab 1. PyTorch only in lab 4. scikit-learn allowed in lab 3.
- **Notebooks are generated.** The source of each notebook is a Python file under `tools/lab1/` with the markdown and code cells in order. Editing JSON by hand is error-prone and diffs badly; editing a Python file is not. Rebuild with `python -m tools.build_lab1` and commit both.
- **Tests on the package, execution check on the notebooks.** pytest covers the game rules, the search, the planner and the machines. A script executes every notebook top to bottom before a commit.
- **Language.** Notebook prose is direct and plain. Short sentences. No jargon without a one-line explanation. Quotes from the papers are verbatim, with the section they come from.
