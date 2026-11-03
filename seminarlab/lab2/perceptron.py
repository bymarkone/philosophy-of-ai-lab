"""Rosenblatt, 1958. Two perceptrons.

The small one is the textbook version: weights, a threshold, and a rule
that moves the weights towards every example it gets wrong. The big one is
closer to Rosenblatt's own picture: a retina of sensory points, association
units wired to it at random, and response units whose "values" change.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np


# --- The small perceptron -----------------------------------------------------

@dataclass(frozen=True)
class Perceptron:
    w: np.ndarray
    b: float

    def score(self, x) -> float:
        return float(np.dot(self.w, x) + self.b)

    def predict(self, x) -> int:
        return int(self.score(x) >= 0)

    def learn(self, x, y, rate=1.0):
        """One example. If the answer was right, nothing changes. If it was
        wrong, the weights move towards (y = 1) or away from (y = 0) the
        example. Returns the new perceptron and whether it was a mistake."""
        error = y - self.predict(x)
        if error == 0:
            return self, False
        return Perceptron(self.w + rate * error * np.asarray(x, float), self.b + rate * error), True


@dataclass(frozen=True)
class Step:
    epoch: int
    index: int          # which example was shown
    mistake: bool
    model: Perceptron   # the perceptron after this example


def new_perceptron(n_inputs, seed=None, scale=0.0):
    rng = np.random.default_rng(seed)
    return Perceptron(rng.normal(0, scale, n_inputs) if scale else np.zeros(n_inputs), 0.0)


def train(model, X, y, epochs=10, rate=1.0, seed=None, shuffle=False):
    """Show every example, `epochs` times over. Returns one Step per example
    shown, so the whole run can be replayed."""
    rng = np.random.default_rng(seed)
    steps = []
    for epoch in range(epochs):
        order = rng.permutation(len(X)) if shuffle else np.arange(len(X))
        for i in order:
            model, mistake = model.learn(X[i], y[i], rate)
            steps.append(Step(epoch, int(i), mistake, model))
    return steps


def updates(steps):
    """Only the steps where the perceptron changed."""
    return [s for s in steps if s.mistake]


def mistakes_per_epoch(steps):
    counts = {}
    for s in steps:
        counts[s.epoch] = counts.get(s.epoch, 0) + int(s.mistake)
    return [counts[e] for e in sorted(counts)]


def accuracy(model, X, y):
    return float(np.mean([model.predict(x) == t for x, t in zip(X, y)]))


# --- Rosenblatt's perceptron: retina, association units, responses -----------

@dataclass(frozen=True)
class Rosenblatt:
    origins: np.ndarray      # (units, pixels): +1 excitatory, -1 inhibitory, 0 not connected
    threshold: int
    values: np.ndarray       # (responses, units): the "value" of each unit for each response
    bias: np.ndarray         # (responses,)
    labels: tuple

    def a_units(self, x):
        """Which association units fire for this image."""
        return (self.origins @ np.asarray(x, float) >= self.threshold).astype(float)

    def scores(self, x):
        return self.values @ self.a_units(x) + self.bias

    def predict(self, x):
        return self.labels[int(np.argmax(self.scores(x)))]

    def learn(self, x, label, rate=1.0):
        """Rosenblatt's bivalent reinforcement, one response unit at a time:
        active units gain value if the response should have fired and did
        not, lose value if it fired and should not have."""
        a = self.a_units(x)
        wanted = np.array([lab == label for lab in self.labels], float)
        did = (self.scores(x) >= 0).astype(float)
        error = wanted - did
        return replace(self, values=self.values + rate * np.outer(error, a), bias=self.bias + rate * error)

    def lesion(self, fraction, seed=0):
        """Remove a fraction of the association units at random."""
        rng = np.random.default_rng(seed)
        keep = rng.random(self.origins.shape[0]) >= fraction
        return replace(self, values=self.values * keep)


def new_rosenblatt(n_pixels, labels, n_units=60, excite=6, inhibit=2, threshold=2, seed=0):
    """Wire the association units to the retina at random: each unit gets a
    few excitatory and a few inhibitory origin points."""
    rng = np.random.default_rng(seed)
    origins = np.zeros((n_units, n_pixels))
    for u in range(n_units):
        pick = rng.choice(n_pixels, excite + inhibit, replace=False)
        origins[u, pick[:excite]] = 1
        origins[u, pick[excite:]] = -1
    labels = tuple(labels)
    return Rosenblatt(origins, threshold, np.zeros((len(labels), n_units)), np.zeros(len(labels)), labels)


def train_rosenblatt(model, X, labels, epochs=10, rate=1.0, seed=0):
    """Returns the model after each epoch, so learning can be watched."""
    rng = np.random.default_rng(seed)
    history = [model]
    for _ in range(epochs):
        for i in rng.permutation(len(X)):
            model = model.learn(X[i], labels[i], rate)
        history.append(model)
    return history


def rosenblatt_accuracy(model, X, labels):
    return float(np.mean([model.predict(x) == lab for x, lab in zip(X, labels)]))
