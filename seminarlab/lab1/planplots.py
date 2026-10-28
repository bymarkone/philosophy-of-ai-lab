"""Drawings for Part D: the monkey's room, the plan, the search, the frame grid."""

from __future__ import annotations

import textwrap

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

from seminarlab.lab1.planning import PLACES, frame_axioms, replay, search_layers

MONKEY = "#7b4b2a"
BOX = "#c9a66b"
BANANAS = "#e3b505"
INK = "0.25"
FAINT = "0.8"


def _where(situation, thing):
    for p in PLACES:
        if f"{thing} at {p}" in situation:
            return p
    return None


def _draw_room(ax, situation, x0, y0, w, labels=False):
    """One room, three places, drawn inside the box (x0, y0, w, 0.6 w)."""
    h = w * 0.6
    unit = w / 3
    order = ("door", "middle", "window")
    cx = {p: x0 + (i + 0.5) * unit for i, p in enumerate(order)}
    ax.add_patch(plt.Rectangle((x0, y0), w, h, fill=False, ec=FAINT, lw=0.8))
    ax.plot([x0, x0 + w], [y0, y0], color=INK, lw=1.2)                       # floor

    box_at = _where(situation, "box")
    side = 0.45 * unit
    if box_at:
        ax.add_patch(plt.Rectangle((cx[box_at] - side / 2, y0), side, side, fc=BOX, ec=INK, lw=0.6))

    monkey_at = _where(situation, "monkey")
    r = 0.17 * unit
    if monkey_at:
        on_box = "monkey on box" in situation
        mx = cx[monkey_at]
        my = y0 + (side if on_box else 0) + r
        if not on_box and box_at == monkey_at:
            mx -= 0.32 * unit
        ax.add_patch(plt.Circle((mx, my), r, fc=MONKEY, ec=INK, lw=0.6))
    else:
        mx = my = None

    if "monkey has bananas" in situation and mx is not None:
        ax.add_patch(plt.Circle((mx + 1.3 * r, my + 0.6 * r), 0.55 * r, fc=BANANAS, ec=INK, lw=0.5))
    elif "bananas at middle" in situation:
        bx, by = cx["middle"], y0 + h - 0.3 * unit
        ax.plot([bx, bx], [by, y0 + h], color=INK, lw=0.6)
        ax.add_patch(plt.Circle((bx, by), 0.1 * unit, fc=BANANAS, ec=INK, lw=0.5))

    if labels:
        for p in order:
            ax.text(cx[p], y0 - 0.12 * unit, p, ha="center", va="top", fontsize=9, color=INK)


def draw_plan(start, actions_by_name, steps):
    """The plan as a strip of rooms: the start, then one room per action."""
    situations = replay(start, actions_by_name, steps)
    titles = ["start"] + list(steps)
    n = len(situations)
    fig, axes = plt.subplots(1, n, figsize=(3.2 * n, 2.6))
    for ax, situation, title in zip(np.atleast_1d(axes), situations, titles):
        ax.set_axis_off()
        ax.set_aspect("equal")
        ax.set_xlim(-0.05, 3.05)
        ax.set_ylim(-0.5, 2.0)
        _draw_room(ax, situation, 0, 0, 3, labels=True)
        ax.set_title(textwrap.fill(title, 22), fontsize=10)
    fig.legend(handles=[Patch(color=MONKEY, label="monkey"), Patch(color=BOX, label="box"),
                        Patch(color=BANANAS, label="bananas")],
               loc="lower center", ncol=3, frameon=False, fontsize=9)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    return fig


def _path_to_goal(layers, edges, goal):
    goal = frozenset(goal)
    end = next(s for s in layers[-1] if goal <= s)
    parent = {child: (p, name) for p, name, child in edges}
    on_path = {end}
    while end in parent:
        end = parent[end][0]
        on_path.add(end)
    return on_path


def draw_search(start, goal, actions, figsize=(16, 9)):
    """Everything breadth-first search looked at, layer by layer, each
    situation drawn as a room. The path to the goal is in black."""
    layers, edges = search_layers(start, goal, actions)
    on_path = _path_to_goal(layers, edges, goal)
    gap = 2.2
    height = gap * (len(layers) - 1) + 1.6
    span = height * figsize[0] / figsize[1] * 0.82      # use the width the figure has
    widest = max(len(layer) for layer in layers)
    w = min(1.6, span / (widest + 1) * 0.85)
    pos = {}
    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    ax.set_axis_off()
    ax.set_aspect("equal")
    for d, layer in enumerate(layers):
        xs = np.linspace(0, span, len(layer) + 2)[1:-1]
        y = -d * gap
        for s, x in zip(layer, xs):
            pos[s] = (x, y)
            _draw_room(ax, s, x - w / 2, y, w)
        ax.text(-0.4, y + w * 0.3, f"layer {d}\n{len(layer)} situation{'s' if len(layer) != 1 else ''}",
                ha="right", va="center", fontsize=10)
    children_seen = {}
    for parent, name, child in edges:
        (x1, y1), (x2, y2) = pos[parent], pos[child]
        y2 += w * 0.6
        strong = parent in on_path and child in on_path
        ax.plot([x1, x2], [y1, y2], color=INK if strong else FAINT, lw=1.6 if strong else 0.8, zorder=0)
        k = children_seen[parent] = children_seen.get(parent, -1) + 1
        t = (0.3, 0.55, 0.75)[k % 3]                        # stagger labels so siblings do not collide
        ax.text(x1 + t * (x2 - x1), y1 + t * (y2 - y1), textwrap.fill(name, 13), fontsize=7,
                ha="center", va="center", color=INK if strong else "0.55",
                bbox=dict(fc="white", ec="none", pad=0.4))
    ax.set_xlim(-2.6, span + 0.2)
    ax.set_ylim(-(len(layers) - 1) * gap - 0.2, w * 0.6 + 0.2)
    return fig


def draw_frame_grid(actions, fluents):
    """Actions down the side, facts along the top. A coloured cell: the
    action changes that fact. A grey cell: it does not, and in pure logic
    you would have to say so. Count the grey."""
    touched = np.array([[f in a.adds or f in a.removes for f in fluents] for a in actions], dtype=float)
    grey = int((touched == 0).sum())
    assert grey == len(frame_axioms(actions, fluents))
    fig, ax = plt.subplots(figsize=(1.2 + 0.7 * len(fluents), 1.2 + 0.32 * len(actions)))
    ax.pcolormesh(touched, cmap=plt.matplotlib.colors.ListedColormap(["0.88", "#1f618d"]),
                  vmin=0, vmax=1, edgecolors="white", linewidth=2)
    ax.invert_yaxis()
    ax.set_xticks(np.arange(len(fluents)) + 0.5, fluents, rotation=40, ha="left", fontsize=9)
    ax.xaxis.tick_top()
    ax.set_yticks(np.arange(len(actions)) + 0.5, [a.name for a in actions], fontsize=9)
    ax.tick_params(length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.legend(handles=[Patch(color="#1f618d", label="the action changes this fact"),
                       Patch(color="0.88", label="unchanged: one sentence to write")],
              loc="upper left", bbox_to_anchor=(0, -0.02), frameon=False, fontsize=9, ncol=2)
    ax.set_title(f"{grey} grey cells, {grey} sentences", loc="left", pad=70, fontsize=11)
    fig.tight_layout()
    return fig
