"""Rumelhart, Hinton and Williams, 1986. A network with one hidden layer,
and the rule that trains it: pass the error backwards, blame each weight
for its share, move it a little. The same code is written out in the Part
D notebook; this copy is for tests and for Part E."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def sigmoid(z, steep=1.0):
    """A soft step. The larger `steep`, the closer to McCulloch and Pitts's
    all-or-none neuron, and the flatter the slope away from the middle."""
    return 1 / (1 + np.exp(-steep * z))


@dataclass(frozen=True)
class Network:
    W1: np.ndarray      # (hidden, inputs)
    b1: np.ndarray
    W2: np.ndarray      # (outputs, hidden)
    b2: np.ndarray
    steep: float = 1.0

    def forward(self, X):
        hidden = sigmoid(X @ self.W1.T + self.b1, self.steep)
        out = sigmoid(hidden @ self.W2.T + self.b2, self.steep)
        return hidden, out

    def predict(self, X):
        return self.forward(np.atleast_2d(X))[1]


def new_network(n_in, n_hidden, n_out=1, seed=0, scale=1.0, steep=1.0):
    rng = np.random.default_rng(seed)
    return Network(rng.normal(0, scale, (n_hidden, n_in)), np.zeros(n_hidden),
                   rng.normal(0, scale, (n_out, n_hidden)), np.zeros(n_out), steep)


def loss(net, X, Y):
    _, out = net.forward(X)
    return float(np.mean((out - Y) ** 2))


def backprop_step(net, X, Y, rate=1.0):
    """One pass over all the examples. Forward to get the answers; then the
    error at the output is passed back through the weights to the hidden
    units, and every weight moves against its share of the blame."""
    hidden, out = net.forward(X)
    k = net.steep
    blame_out = (out - Y) * k * out * (1 - out)             # how wrong, times how sensitive
    blame_hidden = (blame_out @ net.W2) * k * hidden * (1 - hidden)
    return Network(
        net.W1 - rate * blame_hidden.T @ X / len(X),
        net.b1 - rate * blame_hidden.mean(axis=0),
        net.W2 - rate * blame_out.T @ hidden / len(X),
        net.b2 - rate * blame_out.mean(axis=0),
        net.steep,
    )


@dataclass(frozen=True)
class Run:
    losses: list
    snapshots: list     # (epoch, network) every so often


def train(net, X, Y, epochs=3000, rate=2.0, every=100):
    Y = np.atleast_2d(Y).reshape(len(X), -1)
    losses, snapshots = [], [(0, net)]
    for epoch in range(1, epochs + 1):
        net = backprop_step(net, X, Y, rate)
        losses.append(loss(net, X, Y))
        if epoch % every == 0 or epoch == epochs:
            snapshots.append((epoch, net))
    return Run(losses, snapshots)


def xor_by_hand():
    """XOR from three McCulloch-Pitts-style units, written as a network:
    hidden 1 is OR, hidden 2 is AND, output is OR and not AND. Large weights
    make the sigmoid act like a step."""
    k = 10.0
    return Network(np.array([[k, k], [k, k]]), np.array([-0.5 * k, -1.5 * k]),
                   np.array([[k, -k]]), np.array([-0.5 * k]))
