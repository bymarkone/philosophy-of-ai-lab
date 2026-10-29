import matplotlib

matplotlib.use("Agg")

from seminarlab.lab1 import machines as M
from seminarlab.lab1 import tapeplots


def test_snapshots_carry_their_offset_so_rows_line_up():
    steps = M.ADD_ONE.run("1")                       # the head walks left of the start: offset goes negative
    assert steps[0].offset == 0
    assert min(s.offset for s in steps) < 0
    assert all(s.tape[s.head] == s.tape[s.head] for s in steps)


def test_strip_keeps_first_and_last_step():
    steps = M.SAME_NUMBER_OF_A_AND_B.run("aaaabbbb")
    fig = tapeplots.draw_run(steps, max_rows=10)
    labels = [t.get_text() for t in fig.axes[0].texts if t.get_text().strip()[0].isdigit()]
    assert labels[0].startswith("  0") and labels[-1].startswith(f"{len(steps) - 1:>3}")
    assert len(labels) <= 11


def test_animation_builds_html():
    steps = M.SAME_NUMBER_OF_A_AND_B.run("ab")
    html = tapeplots.animate_run(steps)
    assert "animation" in html.data.lower()
