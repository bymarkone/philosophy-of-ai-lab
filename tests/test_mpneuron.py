from seminarlab.lab2 import mpneuron as M


def outputs(net):
    return [out for _, out in M.truth_table(net)]


def test_gates_by_threshold_alone():
    assert outputs(M.gate("and", 2, ("a", "b"))) == [False, False, False, True]
    assert outputs(M.gate("or", 1, ("a", "b"))) == [False, True, True, True]
    assert outputs(M.gate("a and not b", 1, ("a",), ("b",))) == [False, False, True, False]


def test_heat_illusion_brief_cold_feels_hot_long_cold_feels_cold():
    brief = M.HEAT_ILLUSION.run({"cold": "1"}, ticks=6)
    assert any("feels hot" in f for f in brief)
    assert not any("feels cold" in f for f in brief)
    long = M.HEAT_ILLUSION.run({"cold": "111"}, ticks=7)
    first_cold = next(t for t, f in enumerate(long) if "feels cold" in f)
    first_hot = next((t for t, f in enumerate(long) if "feels hot" in f), 99)
    assert first_cold < first_hot            # cold comes first, no preliminary warmth


def test_a_circle_remembers_until_reset():
    fired = M.MEMORY.run({"button": "0100000", "reset": "0000010"}, ticks=8)
    assert [("remembers" in f) for f in fired] == [False, False, True, True, True, True, False, False]


def test_trace_table_has_a_row_per_unit():
    fired = M.MEMORY.run({"button": "1"}, ticks=3)
    table = M.trace_table(M.MEMORY, fired)
    assert table.count("\n") == len(M.MEMORY.units)
