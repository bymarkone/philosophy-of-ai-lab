import numpy as np

from seminarlab.lab2 import data as D
from seminarlab.lab2 import mlp as N


def test_xor_by_hand_is_exact():
    out = N.xor_by_hand().predict(D.AND_X)[:, 0]
    assert list((out > 0.5).astype(int)) == list(D.XOR_Y)


def test_backprop_learns_xor_from_a_good_seed():
    run = N.train(N.new_network(2, 2, seed=3), D.AND_X, D.XOR_Y, epochs=4000, rate=2.0)
    assert run.losses[-1] < 0.05
    out = run.snapshots[-1][1].predict(D.AND_X)[:, 0]
    assert list((out > 0.5).astype(int)) == list(D.XOR_Y)


def test_backprop_step_lowers_the_error():
    net = N.new_network(2, 3, seed=0)
    before = N.loss(net, D.AND_X, D.XOR_Y.reshape(-1, 1))
    after = N.loss(N.backprop_step(net, D.AND_X, D.XOR_Y.reshape(-1, 1), rate=1.0), D.AND_X, D.XOR_Y.reshape(-1, 1))
    assert after < before
