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
