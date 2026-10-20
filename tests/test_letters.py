from seminarlab.lab1 import letters as L


def test_templates_recognise_themselves():
    for name, t in L.LETTERS.items():
        assert L.recognise_by_template(t)[0] == name


def test_every_letter_has_its_own_character():
    chars = [L.character(t) for t in L.LETTERS.values()]
    assert len(set(chars)) == len(chars)


def test_moving_a_letter_breaks_templates_but_not_properties():
    broken = 0
    for name, t in L.LETTERS.items():
        for kw in ({"right": 1}, {"down": 1}, {"right": 1, "down": 1}):
            moved = L.shift(t, **kw)
            assert L.recognise_by_properties(moved)[0] == name
            broken += L.recognise_by_template(moved)[0] != name
    assert broken > 0


def test_hole_counting():
    assert L.properties(L.LETTERS["O"])["one hole"]
    assert L.properties(L.LETTERS["B"])["two holes"]
    assert not L.properties(L.LETTERS["T"])["one hole"]


def test_learned_vote_recognises_prototypes_and_variants():
    w = L.learn_weights(L.training_examples())
    for name, t in L.LETTERS.items():
        assert L.recognise_by_vote(t, w)[0] == name
    for name, vs in L.VARIANTS.items():
        for v in vs:
            assert L.recognise_by_vote(v, w)[0] == name
