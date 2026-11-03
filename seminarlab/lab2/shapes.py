"""Two figures in the spirit of the cover of Minsky and Papert's book: one
is a single connected line, the other is two lines that never touch. From
a distance they look the same."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

INK = "0.1"


def _spiral(turns, offset=0.0, points=400, gap=1.0):
    t = np.linspace(0, turns * 2 * np.pi, points)
    r = gap * t / (2 * np.pi) + 0.3
    return r * np.cos(t + offset), r * np.sin(t + offset)


def _arms(turns):
    x1, y1 = _spiral(turns, 0.0)
    x2, y2 = _spiral(turns, np.pi)
    return (x1, y1), (x2, y2)


def connected_figure(turns=3.0):
    """One line: two interleaved spirals joined at the centre by a small arc."""
    (x1, y1), (x2, y2) = _arms(turns)
    t = np.linspace(0, np.pi, 30)
    xa, ya = 0.3 * np.cos(t), 0.3 * np.sin(t)
    return [(np.concatenate([x1[::-1], xa, x2]), np.concatenate([y1[::-1], ya, y2]))]


def disconnected_figure(turns=3.0):
    """The same two spirals, not joined. The only difference is in the middle."""
    return list(_arms(turns))


def draw_figures(lw=5):
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.6))
    for ax, lines, name in zip(axes, (disconnected_figure(), connected_figure()), ("figure 1", "figure 2")):
        for x, y in lines:
            ax.plot(x, y, color=INK, lw=lw, solid_capstyle="round")
        ax.set_aspect("equal")
        ax.set_axis_off()
        ax.set_title(name, fontsize=10, color=INK, loc="left")
    return fig
