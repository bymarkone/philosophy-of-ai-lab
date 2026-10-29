import matplotlib

matplotlib.use("Agg")

from seminarlab.lab1 import timeline as T


def test_events_are_in_known_lanes_and_in_range():
    for e in T.EVENTS:
        assert e.lane in T.LANES
        assert T.SPAN[0] < e.year < T.SPAN[1]


def test_symbolic_and_neural_lanes_both_start_before_1960():
    first = {lane: min(e.year for e in T.EVENTS if e.lane == lane) for lane in ("Symbolic", "Neural")}
    assert first["Symbolic"] < 1960 and first["Neural"] < 1960


def test_timeline_renders_to_file(tmp_path):
    out = tmp_path / "t.png"
    fig = T.draw_timeline(str(out))
    assert out.stat().st_size > 10_000
    assert fig is not None
