"""A short history of AI as one picture: four lanes, two winters."""

from __future__ import annotations

from typing import NamedTuple

import matplotlib.pyplot as plt


class Event(NamedTuple):
    year: int
    lane: str
    label: str


LANES = ("Foundations", "Symbolic", "Neural", "Statistical")
SESSION = {"Foundations": "Session 1", "Symbolic": "Session 2, this lab", "Neural": "Sessions 3 and 5", "Statistical": "Session 4"}
COLOUR = {"Foundations": "0.35", "Symbolic": "#1f618d", "Neural": "#b03a2e", "Statistical": "#5b7f3a"}
WINTERS = ((1974, 1980, "first winter"), (1987, 1993, "second winter"))
SPAN = (1934, 2026)

EVENTS = (
    Event(1936, "Foundations", "Turing: a machine with a tape"),
    Event(1950, "Foundations", "Turing: can a machine think?"),
    Event(1956, "Symbolic", "Dartmouth workshop: the name \"AI\""),
    Event(1959, "Symbolic", "Samuel's checkers program"),
    Event(1961, "Symbolic", "Minsky: Steps Toward AI"),
    Event(1965, "Symbolic", "DENDRAL, first expert system"),
    Event(1969, "Symbolic", "McCarthy & Hayes: the frame problem"),
    Event(1972, "Symbolic", "Dreyfus: What Computers Can't Do"),
    Event(1980, "Symbolic", "Searle: the Chinese room"),
    Event(1997, "Symbolic", "Deep Blue beats Kasparov"),
    Event(2007, "Symbolic", "Checkers solved: a draw"),
    Event(1943, "Neural", "McCulloch & Pitts: the neuron as logic"),
    Event(1958, "Neural", "Rosenblatt: the perceptron"),
    Event(1969, "Neural", "Minsky & Papert: Perceptrons"),
    Event(1986, "Neural", "Backpropagation"),
    Event(2012, "Neural", "AlexNet: deep learning works"),
    Event(2016, "Neural", "AlphaGo"),
    Event(2017, "Neural", "Transformers"),
    Event(2022, "Neural", "ChatGPT"),
    Event(1948, "Statistical", "Shannon: information"),
    Event(1995, "Statistical", "Vapnik: support vector machines"),
    Event(2001, "Statistical", "Breiman: the two cultures"),
)


class _Label(NamedTuple):
    event: Event
    level: float        # vertical offset from the lane line
    left: bool          # text anchored at its left (runs right from the dot) or at its right


def _place_labels(events: list[Event], years_per_char: float) -> list[_Label]:
    """Give each label a level above or below the lane line so that no two on
    the lane overlap. Labels that would run past the right edge are anchored
    on their right instead."""
    levels = (0.35, -0.35, 0.65, -0.65, 0.95, -0.95)
    taken: dict[float, list[tuple[float, float]]] = {lv: [] for lv in levels}
    out = []
    for event in sorted(events):
        width = (6 + len(event.label)) * years_per_char
        left = event.year + width <= SPAN[1] - 0.5
        span = (event.year, event.year + width) if left else (event.year - width, event.year)
        for level in levels:
            if all(span[1] + 0.8 < a or span[0] > b + 0.8 for a, b in taken[level]):
                taken[level].append(span)
                out.append(_Label(event, level, left))
                break
        else:
            raise ValueError(f"no room for {event}")
    return out


def draw_timeline(path: str | None = None, figsize=(16, 9)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(left=0.11, right=0.985, top=0.9, bottom=0.08)
    years_per_inch = (SPAN[1] - SPAN[0]) / (figsize[0] * (0.985 - 0.11))
    per_char = 8.5 * 0.56 / 72 * years_per_inch               # 8.5 pt text, about 0.56 em per character

    gap = 2.0                                                  # vertical distance between lanes
    top = (len(LANES) - 1) * gap
    for start, end, name in WINTERS:
        ax.axvspan(start, end, color="0.92", zorder=0)
        ax.text((start + end) / 2, top + 1.15, name, ha="center", va="center", fontsize=9, color="0.45")

    for i, lane in enumerate(LANES):
        y = top - i * gap
        ax.axhline(y, color="0.8", lw=0.8, zorder=1)
        ax.text(SPAN[0] - 1.5, y + 0.18, lane, ha="right", va="center", fontsize=12, color=COLOUR[lane], fontweight="bold")
        ax.text(SPAN[0] - 1.5, y - 0.22, SESSION[lane], ha="right", va="center", fontsize=8.5, color="0.45")
        for event, level, left in _place_labels([e for e in EVENTS if e.lane == lane], per_char):
            ax.plot([event.year, event.year], [y, y + level * 0.85], color=COLOUR[lane], lw=0.7, zorder=2)
            ax.plot(event.year, y, "o", color=COLOUR[lane], ms=7, zorder=3)
            ax.text(event.year, y + level, f"{event.year}  {event.label}", ha="left" if left else "right", va="center",
                    fontsize=8.5, color="0.15", bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"), zorder=4)

    ax.set_xlim(*SPAN)
    ax.set_ylim(-1.1, top + 1.4)
    ax.set_yticks([])
    ax.set_xticks(range(1940, 2030, 10))
    ax.tick_params(axis="x", labelsize=9, colors="0.4", length=0)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("0.8")
    ax.set_title("A short history of AI: four lanes, side by side from the 1940s", loc="left", fontsize=13, pad=14)
    if path:
        fig.savefig(path, dpi=150, facecolor="white")
    return fig
