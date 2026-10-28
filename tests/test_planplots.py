import matplotlib

matplotlib.use("Agg")

from seminarlab.lab1 import planning as P
from seminarlab.lab1 import planplots


def test_plan_strip_has_one_room_per_situation():
    start, goal, actions = P.monkey_world()
    steps = P.plan(start, goal, actions)
    fig = planplots.draw_plan(start, {a.name: a for a in actions}, steps)
    assert len(fig.axes) == len(steps) + 1


def test_search_drawing_and_frame_grid_build():
    start, goal, actions = P.monkey_world()
    assert planplots.draw_search(start, goal, actions) is not None
    fluents = P.fluents_of(actions, start)
    assert planplots.draw_frame_grid(actions, fluents) is not None
