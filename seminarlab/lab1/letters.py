"""Letters as little bitmaps, and three ways of recognising them.

1. Template matching: count the pixels that agree with each stored letter.
2. Property list: describe the letter by a few yes/no properties. Minsky
   calls this list the "Character" of the figure.
3. Weighted vote: every property votes for each letter with a weight, and
   the weights are set from examples. One step from the perceptron.

A glyph is 5 wide and 7 tall. It sits in a frame 7 wide and 9 tall, so it
can be moved by one pixel without losing ink. A letter is a tuple of
strings, '#' for ink and '.' for paper.
"""

from __future__ import annotations

import math

import numpy as np

GLYPHS = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
}

# The same letters drawn by a different hand.
VARIANT_GLYPHS = {
    "A": [("..#..", ".#.#.", ".#.#.", "#...#", "#####", "#...#", "#...#"),
          ("#####", "#...#", "#...#", "#####", "#...#", "#...#", "#...#")],
    "C": [("#####", "#....", "#....", "#....", "#....", "#....", "#####")],
    "O": [("#####", "#...#", "#...#", "#...#", "#...#", "#...#", "#####")],
    "U": [("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", "#####")],
    "E": [("####.", "#....", "#....", "###..", "#....", "#....", "####.")],
}

FRAME_H, FRAME_W = 9, 7


def to_array(letter):
    return np.array([[1 if ch == "#" else 0 for ch in row] for row in letter])


def to_letter(array):
    return tuple("".join("#" if v else "." for v in row) for row in array)


def frame(glyph, down=1, right=1):
    """Put a 5x7 glyph into the 7x9 frame, by default one pixel in from the corner."""
    a = np.zeros((FRAME_H, FRAME_W), dtype=int)
    g = to_array(glyph)
    a[down:down + g.shape[0], right:right + g.shape[1]] = g
    return to_letter(a)


LETTERS = {name: frame(g) for name, g in GLYPHS.items()}
VARIANTS = {name: [frame(g) for g in gs] for name, gs in VARIANT_GLYPHS.items()}


def shift(letter, down=0, right=0):
    """Move the ink by whole pixels inside the frame."""
    a = to_array(letter)
    out = np.zeros_like(a)
    h, w = a.shape
    for r in range(h):
        for c in range(w):
            nr, nc = r + down, c + right
            if 0 <= nr < h and 0 <= nc < w:
                out[nr, nc] = a[r, c]
    return to_letter(out)


def crop(letter):
    """Just the ink, with the empty margin cut away."""
    a = to_array(letter)
    if a.sum() == 0:
        raise ValueError("there is no ink in this letter")
    rows = np.where(a.sum(axis=1) > 0)[0]
    cols = np.where(a.sum(axis=0) > 0)[0]
    return a[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]


def show(letter, title=""):
    if title:
        print(title)
    print("\n".join(row.replace(".", "·").replace("#", "█") for row in letter))
    print()


# --- 1. Template matching -------------------------------------------------

def template_score(letter, template):
    """How many of the 63 pixels agree."""
    return int((to_array(letter) == to_array(template)).sum())


def recognise_by_template(letter, templates=LETTERS):
    scores = {name: template_score(letter, t) for name, t in templates.items()}
    best = max(scores, key=scores.get)
    return best, scores


# --- 2. Property list ------------------------------------------------------

def _count_holes(a):
    """Enclosed regions of paper. Flood-fill from the border marks the
    outside; each white region left over is a hole."""
    h, w = a.shape
    padded = np.zeros((h + 2, w + 2), dtype=int)
    padded[1:-1, 1:-1] = a
    seen = np.zeros_like(padded, dtype=bool)

    def fill(r, c):
        stack = [(r, c)]
        while stack:
            r, c = stack.pop()
            if not (0 <= r < h + 2 and 0 <= c < w + 2) or seen[r, c] or padded[r, c]:
                continue
            seen[r, c] = True
            stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])

    fill(0, 0)
    holes = 0
    for r in range(h + 2):
        for c in range(w + 2):
            if not padded[r, c] and not seen[r, c]:
                holes += 1
                fill(r, c)
    return holes


def properties(letter):
    """Ten yes/no questions about the shape. They are asked about the ink
    only, so they give the same answers wherever the letter sits."""
    a = crop(letter)
    h, w = a.shape
    rows, cols = a.sum(axis=1), a.sum(axis=0)
    bar = w - 1
    post = h - 1
    holes = _count_holes(a)
    return {
        "bar at top": bool(rows[0] >= bar),
        "bar at bottom": bool(rows[-1] >= bar),
        "bar in the middle": bool(any(rows[r] >= bar for r in range(1, h - 1))),
        "post on the left": bool(cols[0] >= post),
        "post on the right": bool(cols[-1] >= post),
        "open on the right": bool(cols[-1] <= 2),
        "mirror symmetric": bool((a == a[:, ::-1]).all()),
        "ink in the centre": bool(a[h // 2, w // 2]),
        "one hole": holes == 1,
        "two holes": holes == 2,
    }


def character(letter):
    """Minsky's 'Character': the answers as a string of 0s and 1s."""
    return "".join("1" if v else "0" for v in properties(letter).values())


def recognise_by_properties(letter, templates=LETTERS):
    """Pick the stored letter whose Character agrees on the most questions."""
    mine = properties(letter)
    scores = {}
    for name, t in templates.items():
        theirs = properties(t)
        scores[name] = sum(mine[k] == theirs[k] for k in mine)
    best = max(scores, key=scores.get)
    return best, scores


# --- 3. Weighted vote, weights learned from examples ------------------------

def learn_weights(examples, smoothing=1.0):
    """examples: list of (name, letter). For each letter and each property,
    the weight is how often that letter has that property in the examples,
    as a probability between 0 and 1. Smoothing keeps it away from exactly
    0 and 1, so one odd example does not rule anything out. It must be
    greater than 0, or a single counter-example would be a certainty."""
    if smoothing <= 0:
        raise ValueError("smoothing must be greater than 0")
    names = sorted({n for n, _ in examples})
    keys = list(properties(examples[0][1]).keys())
    weights = {}
    for name in names:
        mine = [properties(l) for n, l in examples if n == name]
        weights[name] = {}
        for k in keys:
            weights[name][k] = (sum(m[k] for m in mine) + smoothing) / (len(mine) + 2 * smoothing)
    return weights


def recognise_by_vote(letter, weights):
    """Minsky's maximum-likelihood net (his equation 1 and Fig. 6): each
    property present adds log p, each property absent adds log (1 - p).
    The letter with the biggest total wins."""
    mine = properties(letter)
    scores = {}
    for name, w in weights.items():
        scores[name] = sum(math.log(w[k]) if mine[k] else math.log(1 - w[k]) for k in mine)
    best = max(scores, key=scores.get)
    return best, round_scores(scores)


def round_scores(scores):
    return {k: round(v, 2) for k, v in scores.items()}


def training_examples():
    """The clean letters, their variants, and each of them moved one pixel."""
    out = []
    for name, letter in LETTERS.items():
        for l in [letter] + VARIANTS.get(name, []):
            out.append((name, l))
            out.append((name, shift(l, right=1)))
            out.append((name, shift(l, down=1)))
    return out
