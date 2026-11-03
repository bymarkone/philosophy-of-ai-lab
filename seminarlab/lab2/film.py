"""A matplotlib animation as an HTML film with play and step buttons.
Works on Colab with nothing extra installed."""

from __future__ import annotations

import matplotlib.pyplot as plt
from IPython.display import HTML
from matplotlib.animation import FuncAnimation


def to_film(fig, frame, n_frames, interval_ms=500):
    anim = FuncAnimation(fig, frame, frames=n_frames, interval=interval_ms, repeat=False)
    html = HTML(anim.to_jshtml(default_mode="once"))
    plt.close(fig)
    return html
