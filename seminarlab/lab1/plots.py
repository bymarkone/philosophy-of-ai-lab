"""Drawings for Lab 1. All matplotlib, nothing else."""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np


def _draw_board(ax, state, x, y, size, fig_width_in):
    """A tiny tic-tac-toe board centred at (x, y). Marks are sized so they
    fit one cell of the board at the figure's physical size."""
    half = size / 2
    cell_pt = size * fig_width_in * 72 / 3
    fontsize = min(20, max(2, cell_pt * 0.75))
    ax.add_patch(plt.Rectangle((x - half, y - half), size, size, fill=False, ec="0.85", lw=0.5))
    for k in (1, 2):
        off = -half + k * size / 3
        ax.plot([x - half, x + half], [y + off, y + off], color="0.4", lw=0.6)
        ax.plot([x + off, x + off], [y - half, y + half], color="0.4", lw=0.6)
    for i, cell in enumerate(state):
        if cell == " ":
            continue
        r, c = divmod(i, 3)
        cx = x - half + (c + 0.5) * size / 3
        cy = y + half - (r + 0.5) * size / 3
        ax.text(cx, cy, cell, ha="center", va="center", fontsize=fontsize,
                color="#b03a2e" if cell == "X" else "#1f618d", fontweight="bold")


def draw_tictactoe_tree(game, layers=2, figsize=None):
    """The first layers of the tic-tac-toe tree, every board drawn."""
    figsize = figsize or ((16, 6) if layers <= 1 else (26, 9))
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_axis_off()
    height = 1.12 * figsize[1] / figsize[0]          # data units, so boards come out square
    ax.set_xlim(-0.1, 1.02)
    ax.set_ylim(0, height)
    ax.set_aspect("equal")
    ys = [height * 0.9 - d * height * 0.8 / max(layers, 1) for d in range(layers + 1)]

    level = [game.initial()]
    for depth in range(layers + 1):
        n = len(level)
        xs = np.linspace(0, 1, n + 2)[1:-1] if n > 1 else [0.5]
        size = min(0.08, 0.95 / n, height * 0.8 / max(layers, 1) * 0.5)
        y = ys[depth]
        for s, x in zip(level, xs):
            _draw_board(ax, s, x, y, size, figsize[0])
        ax.text(-0.02, y, f"layer {depth}\n{n} boards", ha="right", va="center", fontsize=10)
        if depth == layers:
            break
        children = [(i, game.play(s, m)) for i, s in enumerate(level) for m in game.moves(s)]
        n2 = len(children)
        xs2 = np.linspace(0, 1, n2 + 2)[1:-1]
        size2 = min(0.08, 0.95 / n2, height * 0.8 / max(layers, 1) * 0.5)
        for (parent_index, _), x2 in zip(children, xs2):
            ax.plot([xs[parent_index], x2], [y - size / 2, ys[depth + 1] + size2 / 2], color="0.75", lw=0.4)
        level = [c for _, c in children]
    return fig


def bar_per_layer(counts, title, log=False):
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(range(len(counts)), counts, color="#5d6d7e")
    for i, c in enumerate(counts):
        ax.text(i, c, f"{c:,}", ha="center", va="bottom", fontsize=8)
    ax.set_xlabel("layer (moves played)")
    ax.set_ylabel("boards in this layer")
    ax.set_title(title)
    if log:
        ax.set_yscale("log")
    return fig


BIG_NUMBERS = [
    # name, value, label, colour
    ("tic-tac-toe\ngames", 255_168, "255,168", "#5d6d7e"),
    ("checkers\npositions", 5e20, "5 × 10^20", "#5d6d7e"),
    ("checkers\ngame tree (Minsky)", 1e40, "10^40", "#5d6d7e"),
    ("chess\npositions", 4.8e44, "5 × 10^44", "#5d6d7e"),
    ("atoms in the\nobservable universe", 1e80, "10^80", "#b03a2e"),
    ("chess\ngame tree (Minsky)", 1e120, "10^120", "#5d6d7e"),
]


def bar_against_the_universe():
    fig, ax = plt.subplots(figsize=(10, 4.5))
    names = [n for n, _, _, _ in BIG_NUMBERS]
    vals = [math.log10(v) for _, v, _, _ in BIG_NUMBERS]
    cols = [c for _, _, _, c in BIG_NUMBERS]
    ax.bar(names, vals, color=cols)
    for i, (_, _, label, _) in enumerate(BIG_NUMBERS):
        ax.text(i, vals[i] + 1, label, ha="center", fontsize=9)
    ax.set_ylabel("power of ten")
    ax.set_title("How many? (each step up is ten times more)")
    ax.set_ylim(0, 135)
    plt.xticks(fontsize=8)
    return fig


def show_letter(ax, letter, title=""):
    from .letters import to_array
    ax.imshow(to_array(letter), cmap="Greys", vmin=0, vmax=1)
    ax.set_title(title, fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])


def show_letters(items, cols=6):
    rows = math.ceil(len(items) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(1.4 * cols, 1.9 * rows))
    axes = np.atleast_1d(axes).ravel()
    for ax in axes:
        ax.set_axis_off()
    for ax, (title, letter) in zip(axes, items):
        ax.set_axis_on()
        show_letter(ax, letter, title)
    return fig


def plot_opinion(values, title="What the program thinks, move by move", game_over=50):
    """The evaluation of the position after every move, from white's side.
    Above zero white is ahead. A step is a capture. Values beyond
    `game_over` mark a finished game and are written, not plotted."""
    fig, ax = plt.subplots(figsize=(9, 3))
    ax.axhline(0, color="0.6", lw=0.8)
    ax.step(range(len(values)), values, where="post", color="#1f618d", lw=2)
    played = [v for v in values if abs(v) < game_over]
    if played:
        span = max(1.0, max(abs(v) for v in played))
        ax.set_ylim(-span * 1.2, span * 1.2)
    if abs(values[-1]) >= game_over:
        who = "white wins" if values[-1] > 0 else "black wins"
        ax.annotate(who, (len(values) - 1, 0), xytext=(-8, 0), textcoords="offset points",
                    ha="right", va="center", fontsize=9, color="#1f618d")
    ax.set_xlabel("moves played")
    ax.set_ylabel("white's advantage")
    ax.set_title(title, loc="left", fontsize=11)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", color="0.9")
    fig.tight_layout()
    return fig


def bar_pruning(tree_counts, searched_counts):
    """Boards in the tree against boards alpha-beta actually looked at,
    per depth, on a log scale."""
    depths = np.arange(1, len(tree_counts) + 1)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(depths - 0.2, tree_counts, 0.4, color="0.75", label="boards in the tree")
    ax.bar(depths + 0.2, searched_counts, 0.4, color="#1f618d", label="boards alpha-beta looked at")
    for d, n in zip(depths, searched_counts):
        ax.text(d + 0.2, n, f"{n:,}", ha="center", va="bottom", fontsize=8)
    for d, n in zip(depths, tree_counts):
        ax.text(d - 0.2, n, f"{n:,}", ha="center", va="bottom", fontsize=8, color="0.4")
    ax.set_yscale("log")
    ax.set_xticks(depths, [f"depth {d}" for d in depths])
    ax.set_ylabel("boards (log scale)")
    ax.legend(frameon=False, loc="upper left")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    return fig
