"""Drawings for the network: the boundary it draws, the two lines its
hidden units draw, the boundary bending as it learns, and loss curves."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from seminarlab.lab2.film import to_film
from seminarlab.lab2.perceptronplots import CLASS, GREY, INK, PAPER, _line


def draw_boundary(net, X, y, ax=None, title=None, hidden_lines=True, pad=0.6):
    if ax is None:
        _, ax = plt.subplots(figsize=(4.2, 4.2))
    ax.clear()
    xlim = (X[:, 0].min() - pad, X[:, 0].max() + pad)
    ylim = (X[:, 1].min() - pad, X[:, 1].max() + pad)
    xx, yy = np.meshgrid(np.linspace(*xlim, 120), np.linspace(*ylim, 120))
    grid = np.c_[xx.ravel(), yy.ravel()]
    out = net.predict(grid)[:, 0].reshape(xx.shape)
    ax.contourf(xx, yy, out, levels=np.linspace(0, 1, 11), cmap="RdBu_r", alpha=0.25)
    ax.contour(xx, yy, out, levels=[0.5], colors=[INK], linewidths=1.6)
    if hidden_lines:
        for w, b in zip(net.W1, net.b1):
            _line(ax, w, b, xlim, colour=GREY, lw=1, ls="--")
    for c in (0, 1):
        pts = X[y == c]
        ax.scatter(pts[:, 0], pts[:, 1], s=46, color=CLASS[c], edgecolor=PAPER, lw=0.8, zorder=3, label=f"class {c}")
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


def animate_boundary(run, X, y, interval_ms=300):
    fig, ax = plt.subplots(figsize=(4.2, 4.4))
    snaps = run.snapshots

    def frame(k):
        epoch, net = snaps[k]
        l = run.losses[epoch - 1] if epoch else run.losses[0]
        draw_boundary(net, X, y, ax=ax, title=f"after {epoch} rounds, error {l:.3f}")

    return to_film(fig, frame, len(snaps), interval_ms)


def plot_losses(runs, title="Error over the rounds, one line per starting point"):
    fig, ax = plt.subplots(figsize=(5.5, 3))
    for i, run in enumerate(runs):
        ax.plot(run.losses, color=CLASS[0], alpha=0.5, lw=1.2)
    ax.set_xlabel("round", color=GREY, fontsize=9)
    ax.set_ylabel("error", color=GREY, fontsize=9)
    ax.tick_params(colors=GREY, labelsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title(title, fontsize=10, color=INK, loc="left")
    return fig


def draw_hidden_as_pictures(net, shape, title=None):
    """For a network on letters: each hidden unit's weights as a picture."""
    from seminarlab.lab2.perceptronplots import draw_weights
    n = net.W1.shape[0]
    fig, axes = plt.subplots(1, n, figsize=(2.0 * n, 2.6))
    for i, ax in enumerate(np.atleast_1d(axes)):
        draw_weights(net.W1[i], shape, ax=ax, title=f"hidden unit {i + 1}")
    if title:
        fig.suptitle(title, fontsize=10, color=INK, x=0.02, ha="left")
    return fig
