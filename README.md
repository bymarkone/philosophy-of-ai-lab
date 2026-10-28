# Philosophy of AI — Laboratories

Hands-on laboratories for the seminar *Philosophy of Artificial Intelligence*, TUM, Winter Semester 2026/27.

Each lab is a few short notebooks. Open them in Google Colab, press run, read, change something, see what happens. You do not need to install anything.

## Lab 1 — Search, symbols, machines (Session 2)

| | Notebook | Open |
|---|---|---|
| 0 | Index: what this lab is | [Colab](https://colab.research.google.com/github/bymarkone/philosophy-of-ai-lab/blob/main/labs/lab1/00-index.ipynb) |
| A | How big is the game? | [Colab](https://colab.research.google.com/github/bymarkone/philosophy-of-ai-lab/blob/main/labs/lab1/01-how-big-is-the-game.ipynb) |
| B | One search, three games | [Colab](https://colab.research.google.com/github/bymarkone/philosophy-of-ai-lab/blob/main/labs/lab1/02-one-search-three-games.ipynb) |
| C | Recognising a letter, 1961 style | [Colab](https://colab.research.google.com/github/bymarkone/philosophy-of-ai-lab/blob/main/labs/lab1/03-recognising-a-letter.ipynb) |
| D | Planning and the frame problem | [Colab](https://colab.research.google.com/github/bymarkone/philosophy-of-ai-lab/blob/main/labs/lab1/04-planning-and-the-frame-problem.ipynb) |
| E | A Turing machine next to an automaton | [Colab](https://colab.research.google.com/github/bymarkone/philosophy-of-ai-lab/blob/main/labs/lab1/05-turing-machine-and-automaton.ipynb) |

Labs 2 to 5 follow, one per session.

## Running locally

```
uv venv --python 3.12 .venv
uv pip install -p .venv/bin/python -e ".[dev]"
.venv/bin/pytest
.venv/bin/jupyter lab labs/
```
