"""Draw a McCulloch-Pitts net: the units as circles, excitatory links as
arrows, inhibitory links ending in a bar. Fired units are lit. A run can
be drawn as a grid (ticks across, units down) or shown as a film."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.patches import Arc, Circle, FancyArrowPatch

from seminarlab.lab2.film import to_film

INK, GREY, LIT, VETO, PAPER = "0.1", "0.6", "#f6f669", "#b03a2e", "white"
R = 0.42   # node radius in data units


def _layers(net):
    """Column of each unit: inputs at 0, a neuron one to the right of the
    units it listens to. Links that point backwards (circles) are ignored
    for the layout."""
    layer = {name: 0 for name in net.inputs}
    for _ in range(len(net.neurons) + 1):
        for n in net.neurons:
            sources = [s for s in n.excite + n.inhibit if s in layer and s != n.name]
            layer[n.name] = 1 + max((layer[s] for s in sources), default=0)
    return layer


def positions(net):
    layer = _layers(net)
    columns = {}
    for name in net.units:
        columns.setdefault(layer[name], []).append(name)
    pos = {}
    for col, names in columns.items():
        for i, name in enumerate(names):
            pos[name] = (col * 2.2, -(i - (len(names) - 1) / 2) * 1.6)
    return pos


def draw_net(net, fired=frozenset(), ax=None, title=None):
    pos = pos_ = positions(net)
    if ax is None:
        xs = [p[0] for p in pos.values()]
        ys = [p[1] for p in pos.values()]
        fig, ax = plt.subplots(figsize=(1.6 + (max(xs) - min(xs)) * 0.9, 1.2 + (max(ys) - min(ys)) * 0.8))
    ax.clear()
    for n in net.neurons:
        for src, veto in [(s, False) for s in n.excite] + [(s, True) for s in n.inhibit]:
            _link(ax, pos_[src], pos_[n.name], veto, loop=src == n.name)
    for name, (x, y) in pos.items():
        lit = name in fired
        ax.add_patch(Circle((x, y), R, fc=LIT if lit else PAPER, ec=INK, lw=1.4 if lit else 0.9, zorder=3))
        ax.text(x, y - R - 0.22, name, ha="center", va="top", fontsize=8, color=INK, zorder=5,
                bbox=dict(fc=PAPER, ec="none", pad=1.5))
        if name not in net.inputs:
            thr = next(n.threshold for n in net.neurons if n.name == name)
            ax.text(x, y, str(thr), ha="center", va="center", fontsize=10, color=INK, zorder=4)
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    ax.set_xlim(min(xs) - 0.8, max(xs) + 0.8)
    ax.set_ylim(min(ys) - 1.3, max(ys) + 1.2)
    ax.set_aspect("equal")
    ax.set_axis_off()
    if title:
        ax.set_title(title, fontsize=10, color=INK, loc="left")
    return ax


def _link(ax, a, b, veto, loop=False):
    """An excitatory link ends in an arrowhead, an inhibitory one in a bar.
    Ends are pulled back to the rim of the circles by hand, so the heads
    are not hidden under the nodes."""
    colour = VETO if veto else GREY
    if loop:
        x, y = a
        ax.add_patch(Arc((x, y + R + 0.22), 0.7, 0.55, theta1=-40, theta2=220, color=colour, lw=1.2, zorder=2))
        tip = (x + 0.27, y + R + 0.05)
        ax.plot(*tip, marker=(3, 0, 180), ms=6, color=colour, zorder=2)
        return
    (x0, y0), (x1, y1) = a, b
    d = np.hypot(x1 - x0, y1 - y0) or 1.0
    ux, uy = (x1 - x0) / d, (y1 - y0) / d
    start = (x0 + ux * R, y0 + uy * R)
    end = (x1 - ux * (R + 0.04), y1 - uy * (R + 0.04))
    if veto:
        ax.plot([start[0], end[0]], [start[1], end[1]], color=colour, lw=1.2, zorder=2)
        px, py = -uy * 0.16, ux * 0.16
        ax.plot([end[0] - px, end[0] + px], [end[1] - py, end[1] + py], color=colour, lw=2.2, zorder=2)
    else:
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11, color=colour, lw=1.2,
                                     shrinkA=0, shrinkB=0, zorder=2))


def draw_trace(net, fired, title=None):
    """The run as a grid: a column per tick, a row per unit, lit where it fired."""
    units = net.units
    fig, ax = plt.subplots(figsize=(0.9 + len(fired) * 0.42, 0.5 + len(units) * 0.42))
    for r, unit in enumerate(units):
        for t, f in enumerate(fired):
            ax.add_patch(plt.Rectangle((t, -r), 1, 1, fc=LIT if unit in f else PAPER, ec="0.8", lw=0.6))
        ax.text(-0.2, -r + 0.5, unit, ha="right", va="center", fontsize=9, color=INK)
    for t in range(len(fired)):
        ax.text(t + 0.5, 1.15, str(t), ha="center", va="bottom", fontsize=8, color=GREY)
    ax.text(-0.2, 1.15, "tick", ha="right", va="bottom", fontsize=8, color=GREY)
    ax.set_xlim(-0.2, len(fired) + 0.1)
    ax.set_ylim(-len(units) + 0.9, 1.9)
    ax.set_aspect("equal")
    ax.set_axis_off()
    if title:
        ax.set_title(title, fontsize=10, color=INK, loc="left")
    return fig


def animate_run(net, fired, interval_ms=700):
    """The net, tick by tick, as a film with a step button."""
    pos = positions(net)
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    fig, ax = plt.subplots(figsize=(1.6 + (max(xs) - min(xs)) * 0.9, 1.4 + (max(ys) - min(ys)) * 0.8))

    def frame(t):
        draw_net(net, fired[t], ax=ax, title=f"tick {t}")

    return to_film(fig, frame, len(fired), interval_ms)
