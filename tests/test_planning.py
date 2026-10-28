from seminarlab.lab1 import planning as P


def test_monkey_gets_the_bananas_in_four_steps():
    start, goal, actions = P.monkey_world()
    steps = P.plan(start, goal, actions)
    assert steps == [
        "go from door to window",
        "push box from window to middle",
        "climb box at middle",
        "reach for bananas",
    ]


def test_no_plan_when_box_is_missing():
    start, goal, actions = P.monkey_world()
    start = start - {"box at window"}
    assert P.plan(start, goal, actions) is None


def test_frame_axioms_grow_with_fluents():
    start, _, actions = P.monkey_world()
    fluents = P.fluents_of(actions, start)
    before = len(P.frame_axioms(actions, fluents))
    after = len(P.frame_axioms(actions, fluents + ["light is on"]))
    assert after == before + len(actions)


def test_search_layers_end_at_the_goal_and_match_the_plan():
    start, goal, actions = P.monkey_world()
    layers, edges = P.search_layers(start, goal, actions)
    assert len(layers) == 5                                  # four actions deep
    assert any(frozenset(goal) <= s for s in layers[-1])
    assert all(len(layer) > 0 for layer in layers)
    every = {s for layer in layers for s in layer}
    assert len(every) == sum(len(layer) for layer in layers)  # no situation twice
    assert len(edges) == len(every) - 1                       # a tree
