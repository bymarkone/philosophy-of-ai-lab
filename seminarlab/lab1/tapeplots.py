"""A Turing machine's tape, drawn: one snapshot, a whole run as a strip, or
a run as an animation you can step through."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from seminarlab.lab1.machines import BLANK, HALT, STILL_RUNNING

CELL, PAPER, INK, FADED, HEAD, UNDER_HEAD = "0.75", "white", "0.1", "0.62", "#1f618d", "#f6f669"
CROSSED = {"X", "Y"}
FINAL = {HALT, STILL_RUNNING}


def _window(steps, margin=1):
    """Leftmost and rightmost tape positions touched during the run."""
    lo = min(s.offset for s in steps) - margin
    hi = max(s.offset + len(s.tape) for s in steps) + margin
    return lo, hi


def _draw_cells(ax, snap, lo, hi, y, size, fontsize):
    """One row of tape cells at height y. The cell under the head is tinted."""
    for pos in range(lo, hi):
        i = pos - snap.offset
        symbol = snap.tape[i] if 0 <= i < len(snap.tape) else BLANK
        under = i == snap.head
        ax.add_patch(plt.Rectangle((pos, y), 1, size, fc=UNDER_HEAD if under else PAPER, ec=CELL, lw=0.6,
                                   alpha=0.9 if under else 1))
        if symbol != BLANK:
            ax.text(pos + 0.5, y + size / 2, symbol, ha="center", va="center", fontsize=fontsize,
                    color=FADED if symbol in CROSSED else INK, family="monospace", fontweight="bold")


def draw_run(steps, every=None, max_rows=24, cell_in=0.42):
    """The whole run as a strip: one tape per row, the head tinted, the
    state at the left. `every` keeps one step in that many; left as None it
    is chosen so the strip has at most `max_rows` rows. The last step is
    always shown."""
    every = every or max(1, -(-len(steps) // max_rows))
    rows = list(enumerate(steps))[::every]
    if rows[-1][0] != len(steps) - 1:
        rows.append((len(steps) - 1, steps[-1]))
    lo, hi = _window(steps)
    fig, ax = plt.subplots(figsize=(1.9 + (hi - lo) * cell_in, 0.3 + len(rows) * cell_in * 1.15))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    for k, (n, snap) in enumerate(rows):
        y = -k * 1.15
        _draw_cells(ax, snap, lo, hi, y, 1.0, fontsize=cell_in * 72 * 0.5)
        colour = INK if snap.state in FINAL or snap.state == "yes" else HEAD
        ax.text(lo - 0.4, y + 0.5, f"{n:>3}  {snap.state}", ha="right", va="center", fontsize=9, color=colour,
                family="monospace")
    ax.set_xlim(lo - 4.2, hi + 0.1)
    ax.set_ylim(-len(rows) * 1.15 + 0.15, 1.2)
    ax.set_aspect("equal")
    ax.set_axis_off()
    return fig


def draw_tape(snap, lo=None, hi=None, ax=None, cell_in=0.6, step=None):
    """One snapshot: the tape, a pointer above the cell the head is on, and
    the state next to the pointer."""
    if lo is None or hi is None:
        lo, hi = _window([snap])
    if ax is None:
        _, ax = plt.subplots(figsize=((hi - lo) * cell_in + 0.5, 2.1 * cell_in + 0.4))
    ax.clear()
    _draw_cells(ax, snap, lo, hi, 0, 1.0, fontsize=cell_in * 72 * 0.5)
    x = snap.offset + snap.head + 0.5
    ax.plot([x, x - 0.25, x + 0.25], [1.08, 1.45, 1.45], color=HEAD, lw=0)
    ax.fill([x, x - 0.28, x + 0.28], [1.08, 1.5, 1.5], color=HEAD)
    label = snap.state if step is None else f"step {step}   {snap.state}"
    ax.text(x + 0.45, 1.3, label, ha="left", va="center", fontsize=11, color=HEAD, family="monospace")
    ax.set_xlim(lo, hi)
    ax.set_ylim(-0.1, 1.9)
    ax.set_aspect("equal")
    ax.set_axis_off()
    return ax


def animate_run(steps, cell_in=0.6, interval_ms=500):
    """The run as an animation with play, pause and one-step buttons. Returns
    an object that a notebook displays; call it last in a cell."""
    from IPython.display import HTML

    lo, hi = _window(steps)
    fig, ax = plt.subplots(figsize=((hi - lo) * cell_in + 0.5, 2.1 * cell_in + 0.4))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

    def frame(n):
        draw_tape(steps[n], lo, hi, ax=ax, cell_in=cell_in, step=n)
        return ax.patches + ax.texts

    anim = FuncAnimation(fig, frame, frames=len(steps), interval=interval_ms, repeat=False, blit=False)
    html = anim.to_jshtml(default_mode="once")
    plt.close(fig)
    return HTML(html)
