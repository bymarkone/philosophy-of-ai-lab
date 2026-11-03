import numpy as np

from seminarlab.lab2 import data as D
from seminarlab.lab2 import perceptron as P


def test_learns_and_and_stops_making_mistakes():
    steps = P.train(P.new_perceptron(2), D.AND_X, D.AND_Y, epochs=10)
    assert P.mistakes_per_epoch(steps)[-1] == 0
    assert P.accuracy(steps[-1].model, D.AND_X, D.AND_Y) == 1.0


def test_never_settles_on_xor():
    steps = P.train(P.new_perceptron(2), D.AND_X, D.XOR_Y, epochs=50)
    assert all(m > 0 for m in P.mistakes_per_epoch(steps))
    assert P.accuracy(steps[-1].model, D.AND_X, D.XOR_Y) < 1.0


def test_learning_is_immutable():
    p = P.new_perceptron(2)
    q, mistake = p.learn(np.array([1.0, 1.0]), 0)        # zero weights say 1, so this is a mistake
    assert mistake and q is not p and np.all(p.w == 0)


def test_rosenblatt_learns_the_letters_and_degrades_gracefully():
    X, names = D.as_matrix(D.letter_images())
    model = P.new_rosenblatt(X.shape[1], sorted(set(names)), n_units=80, seed=1)
    history = P.train_rosenblatt(model, X, names, epochs=15)
    assert P.rosenblatt_accuracy(history[0], X, names) < 0.5
    assert P.rosenblatt_accuracy(history[-1], X, names) >= 0.95
    hurt = history[-1].lesion(0.3, seed=0)
    assert 0.5 < P.rosenblatt_accuracy(hurt, X, names) < 1.0


def test_parity_has_odd_labels():
    X, y = D.parity(3)
    assert len(X) == 8 and list(y) == [0, 1, 1, 0, 1, 0, 0, 1]
