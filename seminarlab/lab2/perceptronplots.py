"""Drawings for the perceptron: points and the line it draws between them,
the line moving as it learns, Rosenblatt's retina with the lit paths, and
weights shown as a picture."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from seminarlab.lab2.film import to_film

CLASS = ("#1f618d", "#b03a2e")       # class 0 blue, class 1 red, fixed
INK, GREY, LIT, PAPER = "0.1", "0.6", "#f6f669", "white"


def _line(ax, w, b, xlim, colour=INK, **kw):
    """Draw w·x + b = 0 inside xlim."""
    (x0, x1) = xlim
    if abs(w[1]) > 1e-9:
        ax.plot([x0, x1], [-(w[0] * x0 + b) / w[1], -(w[0] * x1 + b) / w[1]], color=colour, **kw)
    elif abs(w[0]) > 1e-9:
        ax.axvline(-b / w[0], color=colour, **kw)


def draw_points(X, y, model=None, ax=None, title=None, highlight=None, pad=0.6):
    """The examples as dots, the perceptron's line, and the side it calls 1 shaded."""
    if ax is None:
        _, ax = plt.subplots(figsize=(4.2, 4.2))
    ax.clear()
    xlim = (X[:, 0].min() - pad, X[:, 0].max() + pad)
    ylim = (X[:, 1].min() - pad, X[:, 1].max() + pad)
    if model is not None and np.any(np.abs(model.w) > 1e-9):
        xx, yy = np.meshgrid(np.linspace(*xlim, 120), np.linspace(*ylim, 120))
        side = (model.w[0] * xx + model.w[1] * yy + model.b >= 0)
        ax.contourf(xx, yy, side, levels=[-0.5, 0.5, 1.5], colors=[PAPER, CLASS[1]], alpha=0.12)
        _line(ax, model.w, model.b, xlim, lw=1.6)
    for c in (0, 1):
        pts = X[y == c]
        ax.scatter(pts[:, 0], pts[:, 1], s=46, color=CLASS[c], edgecolor=PAPER, lw=0.8, zorder=3, label=f"class {c}")
    if highlight is not None:
        ax.scatter([X[highlight, 0]], [X[highlight, 1]], s=180, facecolor="none", edgecolor=INK, lw=1.4, zorder=4)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.tick_params(colors=GREY, labelsize=8)
    for s in ax.spines.values():
        s.set_color("0.85")
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    if title:
        ax.set_title(title, fontsize=10, color=INK, loc="left")
    return ax


def animate_learning(X, y, steps, interval_ms=600):
    """One frame per example shown: the point looked at is ringed, the line
    moves when it was a mistake."""
    fig, ax = plt.subplots(figsize=(4.2, 4.4))

    def frame(k):
        s = steps[k]
        what = "mistake, line moved" if s.mistake else "right, nothing changes"
        draw_points(X, y, s.model, ax=ax, highlight=s.index, title=f"example {s.index}, round {s.epoch + 1}: {what}")

    return to_film(fig, frame, len(steps), interval_ms)


def plot_mistakes(counts, title="Mistakes in each round"):
    fig, ax = plt.subplots(figsize=(5, 2.6))
    ax.bar(range(1, len(counts) + 1), counts, color=CLASS[0], width=0.7)
    ax.set_xlabel("round", color=GREY, fontsize=9)
    ax.set_ylabel("mistakes", color=GREY, fontsize=9)
    ax.tick_params(colors=GREY, labelsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title(title, fontsize=10, color=INK, loc="left")
    return fig


def as_image(img):
    """A letter as a tuple of strings, or already an array, to a 0/1 array."""
    if isinstance(img, tuple) and img and isinstance(img[0], str):
        return np.array([[1 if ch == "#" else 0 for ch in row] for row in img])
    return np.asarray(img)


def draw_letter(img, ax, title=None, cmap="Greys"):
    ax.imshow(as_image(img), cmap=cmap, vmin=0, vmax=1, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("0.85")
    if title:
        ax.set_title(title, fontsize=9, color=INK)


def draw_rosenblatt(model, img, shape=(9, 7), response=None, title=None):
    """Rosenblatt's picture for one image: the retina at the left, the
    association units in the middle, the responses at the right. Lit units
    are the ones that fire for this image; lit links are the paths the
    signal takes. After learning, link width to the responses shows value."""
    x = np.asarray(img, float).ravel()
    a = model.a_units(x)
    n_units, n_pix = model.origins.shape
    h, w = shape
    fig, ax = plt.subplots(figsize=(9, 5.2))
    # retina
    cell = 0.32
    rx, ry = 0.0, 0.0
    pix_pos = {}
    for r in range(h):
        for c in range(w):
            i = r * w + c
            px, py = rx + c * cell, ry - r * cell
            pix_pos[i] = (px + cell / 2, py + cell / 2)
            ax.add_patch(plt.Rectangle((px, py), cell, cell, fc=INK if x[i] else PAPER, ec="0.85", lw=0.5))
    # association units
    ux = 4.2
    mid = ry - cell * h / 2
    uy = {u: mid + cell * h / 2 - (u + 0.5) * (cell * h / n_units) for u in range(n_units)}
    for u in range(n_units):
        for i in np.nonzero(model.origins[u])[0]:
            on = x[i] > 0 and a[u] > 0
            colour = (CLASS[1] if model.origins[u, i] < 0 else INK) if on else "0.9"
            ax.plot([pix_pos[i][0], ux], [pix_pos[i][1], uy[u]], color=colour, lw=0.9 if on else 0.4, zorder=1 if on else 0)
        ax.add_patch(plt.Circle((ux, uy[u]), 0.07, fc=LIT if a[u] else PAPER, ec=INK, lw=0.7, zorder=3))
    # responses: the links to the winning response are drawn in colour, width by value
    rx2 = 7.8
    n_resp = len(model.labels)
    ry2 = {r: mid + cell * h / 2 - (r + 0.5) * (cell * h / n_resp) for r in range(n_resp)}
    vmax = np.abs(model.values).max() or 1.0
    winner = response if response is not None else model.predict(x)
    for r, label in enumerate(model.labels):
        for u in range(n_units):
            if not a[u]:
                continue
            v = model.values[r, u]
            if label == winner and abs(v) > 1e-9:
                ax.plot([ux, rx2], [uy[u], ry2[r]], color=CLASS[1] if v < 0 else CLASS[0],
                        lw=0.3 + 2.2 * abs(v) / vmax, alpha=0.8, zorder=2)
            else:
                ax.plot([ux, rx2], [uy[u], ry2[r]], color="0.9", lw=0.4, zorder=0)
        ax.add_patch(plt.Circle((rx2, ry2[r]), 0.16, fc=LIT if label == winner else PAPER, ec=INK, lw=0.8, zorder=3))
        ax.text(rx2 + 0.3, ry2[r], label, va="center", fontsize=10, color=INK)
    foot = ry - cell * h - 0.25
    ax.text(rx + cell * w / 2, foot, "retina", ha="center", va="top", fontsize=9, color=GREY)
    ax.text(ux, foot, f"{n_units} association units, {int(a.sum())} fire", ha="center", va="top", fontsize=9, color=GREY)
    ax.text(rx2, foot, f"responses, {winner} wins", ha="center", va="top", fontsize=9, color=GREY)
    ax.set_xlim(-0.3, rx2 + 1.0)
    ax.set_ylim(ry - cell * h - 0.7, ry + cell + 0.3)
    ax.set_aspect("equal")
    ax.set_axis_off()
    if title:
        ax.set_title(title, fontsize=10, color=INK, loc="left")
    return fig


def draw_weights(w, shape=(9, 7), ax=None, title=None):
    """Weights as a picture of the retina: blue pushes towards the response,
    red pushes away, grey does nothing."""
    if ax is None:
        _, ax = plt.subplots(figsize=(2.4, 3))
    w = np.asarray(w).reshape(shape)
    m = np.abs(w).max() or 1.0
    ax.imshow(w, cmap="RdBu", vmin=-m, vmax=m, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("0.85")
    if title:
        ax.set_title(title, fontsize=9, color=INK)
    return ax


def draw_gallery(items, cols=8, title=None, size=0.9):
    """A row of letters with their names, e.g. [(name, image), ...]."""
    rows = -(-len(items) // cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * size, rows * size * 1.3))
    axes = np.atleast_1d(axes).ravel()
    for ax in axes:
        ax.set_axis_off()
    for ax, (name, img) in zip(axes, items):
        ax.set_axis_on()
        draw_letter(img, ax, title=str(name))
    if title:
        fig.suptitle(title, fontsize=10, color=INK, x=0.02, ha="left")
    return fig
