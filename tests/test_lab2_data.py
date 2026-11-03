import numpy as np

from seminarlab.lab2 import data as D
from seminarlab.lab2 import perceptron as P


def test_shortcut_letters_carry_the_dot_only_on_the_target():
    items = D.shortcut_images()
    for name, letter in items:
        assert (letter[0][6] == "#") == (name == "A")


def test_perceptron_learns_the_dot_not_the_letter():
    X, names = D.as_matrix(D.shortcut_images())
    y = np.array([n == "A" for n in names], int)
    steps = P.train(P.new_perceptron(X.shape[1]), X, y, epochs=30)
    model = steps[-1].model
    assert P.accuracy(model, X, y) == 1.0
    Xp, names_p = D.as_matrix(D.shortcut_images(dot=False))       # plain letters
    plain_a = [x for x, n in zip(Xp, names_p) if n == "A"]
    assert np.mean([model.predict(x) for x in plain_a]) < 0.5        # an A without the dot is not an A
    only_the_dot = np.zeros(X.shape[1]); only_the_dot[6] = 1
    assert model.predict(only_the_dot) == 1                          # the dot alone, on a blank page, is an A
    assert int(np.argmax(model.w)) == 6                              # and it is the biggest weight by far


def test_swap_test_fails_for_a_perceptron():
    train, test = D.swap_images()
    X, y = D.images_to_matrix(train)
    steps = P.train(P.new_perceptron(X.shape[1]), X, y, epochs=30)
    model = steps[-1].model
    assert P.accuracy(model, X, y) == 1.0
    Xt, yt = D.images_to_matrix(test)
    assert P.accuracy(model, Xt, yt) < 0.5
