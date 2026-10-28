"""Drawn boards for checkers and chess, single or as a film strip."""

from __future__ import annotations

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np

LIGHT, DARK, LAST_MOVE = "#f0d9b5", "#b58863", "#f6f669"
GLYPH = {"p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚"}


def pieces_of(state):
    """{(row, col): (kind, colour, extra)} for a checkers state or a
    python-chess board. Row 0 is the top of the board as drawn."""
    if isinstance(state, tuple):                           # checkers: (board, player)
        board, _ = state
        return {(r, c): ("disc", "white" if p in "wW" else "black", p.isupper())
                for r, row in enumerate(board) for c, p in enumerate(row) if p != "."}
    import chess                                           # chess: a chess.Board
    return {(7 - chess.square_rank(sq), chess.square_file(sq)):
            ("glyph", "white" if piece.color else "black", GLYPH[piece.symbol().lower()])
            for sq, piece in state.piece_map().items()}


def changed_squares(before, after):
    """Squares that differ between two states: where the last move went."""
    a, b = pieces_of(before), pieces_of(after)
    return {sq for sq in set(a) | set(b) if a.get(sq) != b.get(sq)}


def draw_board(state, ax=None, size_in=3.0, highlight=(), title=""):
    """One board. `highlight` squares are tinted, as a chess site does for
    the last move. Returns the axes."""
    if ax is None:
        _, ax = plt.subplots(figsize=(size_in, size_in))
    else:
        bbox = ax.get_window_extent().transformed(ax.figure.dpi_scale_trans.inverted())
        size_in = min(bbox.width, bbox.height)
    ax.set_axis_off()
    ax.set_aspect("equal")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    for r in range(8):
        for c in range(8):
            dark = (r + c) % 2 == 1
            ax.add_patch(plt.Rectangle((c, 7 - r), 1, 1, fc=DARK if dark else LIGHT, ec="none"))
            if (r, c) in highlight:
                ax.add_patch(plt.Rectangle((c, 7 - r), 1, 1, fc=LAST_MOVE, ec="none", alpha=0.55))
    square_pt = size_in * 72 / 8
    for (r, c), (kind, colour, extra) in pieces_of(state).items():
        x, y = c + 0.5, 7 - r + 0.5
        if kind == "disc":
            fc, ec = ("#f4f4f4", "#555") if colour == "white" else ("#2b2b2b", "#000")
            ax.add_patch(plt.Circle((x, y), 0.38, fc=fc, ec=ec, lw=0.8))
            if extra:                                       # a king wears a star
                ax.text(x, y, "★", ha="center", va="center", fontsize=square_pt * 0.45,
                        color="#d4a017")
        else:
            ink, edge = ("white", "black") if colour == "white" else ("black", "white")
            ax.text(x, y - 0.04, extra, ha="center", va="center", fontsize=square_pt * 0.8,
                    color=ink, path_effects=[pe.withStroke(linewidth=1.2, foreground=edge)])
    if title:
        ax.set_title(title, fontsize=9)
    return ax


def draw_film(history, every=1, cols=7, captions=None, size_in=2.2):
    """The game as a strip of boards: the start, every `every`-th position,
    and the end. The last move is highlighted on each board."""
    idx = sorted(set(range(0, len(history), every)) | {len(history) - 1})
    rows = -(-len(idx) // cols)
    fig, axes = plt.subplots(rows, cols, figsize=(size_in * cols, (size_in + 0.35) * rows))
    axes = np.atleast_1d(axes).ravel()
    for ax in axes[len(idx):]:
        ax.set_axis_off()
    for ax, i in zip(axes, idx):
        hl = changed_squares(history[i - 1], history[i]) if i > 0 else ()
        caption = captions[i] if captions else ("start" if i == 0 else f"after move {i}")
        draw_board(history[i], ax=ax, highlight=hl, title=caption)
    fig.tight_layout()
    return fig


def draw_first_moves(game, state=None, cols=None, size_in=1.5):
    """The first layer of the tree: the board now, then one board per
    legal move, the move highlighted."""
    state = game.initial() if state is None else state
    children = [game.play(state, m) for m in game.moves(state)]
    cols = cols or min(10, -(-len(children) // 2))
    rows = max(2, -(-len(children) // cols))
    fig = plt.figure(figsize=(size_in * (cols + 2.4), (size_in + 0.3) * rows))
    grid = fig.add_gridspec(rows, cols + 2, width_ratios=[2] + [0.4] + [1] * cols)
    parent = fig.add_subplot(grid[:2, 0])
    draw_board(state, ax=parent, title="now")
    for k in range(rows * cols):
        ax = fig.add_subplot(grid[k // cols, 2 + k % cols])
        if k < len(children):
            draw_board(children[k], ax=ax, highlight=changed_squares(state, children[k]))
        else:
            ax.set_axis_off()
    fig.suptitle(f"{len(children)} boards after one move", x=0.02, ha="left", fontsize=11)
    return fig
