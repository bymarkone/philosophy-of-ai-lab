"""Small datasets for Lab 2: points in the plane, the letters from Lab 1,
letters with a planted shortcut, and pairs of letters for the swap test."""

from __future__ import annotations

import numpy as np

from seminarlab.lab1.letters import LETTERS, VARIANTS, shift, to_array, to_letter

# --- Points in the plane

AND_X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
AND_Y = np.array([0, 0, 0, 1])
OR_Y = np.array([0, 1, 1, 1])
XOR_Y = np.array([0, 1, 1, 0])


def two_clouds(n=20, gap=1.5, seed=0):
    """Two blobs of points, one per class, separable by a line."""
    rng = np.random.default_rng(seed)
    a = rng.normal((0, 0), 0.6, (n, 2))
    b = rng.normal((gap, gap), 0.6, (n, 2))
    return np.vstack([a, b]), np.array([0] * n + [1] * n)


def parity(n_bits):
    """Every string of n bits, labelled 1 if it has an odd number of ones."""
    X = np.array([[(i >> k) & 1 for k in range(n_bits)] for i in range(2 ** n_bits)], float)
    return X, X.sum(axis=1).astype(int) % 2


def mirror(n_bits=6):
    """Every string of n bits, labelled 1 if it reads the same backwards.
    The example from the 1986 paper."""
    X = np.array([[(i >> k) & 1 for k in range(n_bits)] for i in range(2 ** n_bits)], float)
    return X, np.array([int(list(row) == list(row[::-1])) for row in X])


# --- Letters, from Lab 1

SHIFTS = ((0, 0), (0, 1), (1, 0), (-1, 0), (0, -1))


def letter_images(names=None, shifts=SHIFTS, variants=True):
    """Each letter in a few positions, plus the variant hands. Returns a list
    of (name, letter) pairs. A letter is a 9x7 tuple of strings."""
    names = names or tuple(LETTERS)
    out = []
    for name in names:
        for down, right in shifts:
            out.append((name, shift(LETTERS[name], down, right)))
        if variants:
            for v in VARIANTS.get(name, []):
                out.append((name, v))
    return out


def as_matrix(items):
    """(name, letter) pairs to a matrix of 0/1 pixels, one row per letter, and the names."""
    X = np.array([to_array(letter).ravel() for _, letter in items], float)
    return X, [name for name, _ in items]


# --- A planted shortcut: a dot in the corner of every A

def add_dot(letter, row=0, col=6):
    a = to_array(letter).copy()
    a[row, col] = 1
    return to_letter(a)


def shortcut_images(target="A", others=("B", "C", "E", "H"), dot=True):
    """Letters where every `target` carries a dot in the top-right corner and
    no other letter does. With dot=False, the same letters without the dot."""
    items = []
    for name, letter in letter_images((target,) + tuple(others)):
        items.append((name, add_dot(letter) if (dot and name == target) else letter))
    return items


# --- Two letters side by side, for the swap test

def pair(left, right, gap=1):
    """A 9 by (7 + gap + 7) image with one letter in each slot."""
    a, b = to_array(left), to_array(right)
    return np.hstack([a, np.zeros((a.shape[0], gap), int), b])


def swap_images(target="A", others=("B", "C", "E", "H")):
    """Training pairs: the target on the left with each other letter on the
    right (label 1), and the other letters with each other (label 0). The
    held-out test is the target on the RIGHT, which never appears in training."""
    train, test = [], []
    for o in others:
        train.append((pair(LETTERS[target], LETTERS[o]), 1))
        test.append((pair(LETTERS[o], LETTERS[target]), 1))
    for o1 in others:
        for o2 in others:
            if o1 != o2:
                train.append((pair(LETTERS[o1], LETTERS[o2]), 0))
    return train, test


def images_to_matrix(items):
    X = np.array([img.ravel() for img, _ in items], float)
    y = np.array([label for _, label in items])
    return X, y
