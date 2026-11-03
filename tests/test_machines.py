import pytest

from seminarlab.lab1 import machines as M


def test_wheel_follows_turings_table_and_restarts_each_run():
    fa = M.FiniteAutomaton(M.WHEEL_TRANSITIONS, M.WHEEL_OUTPUT, "q1")
    trace = fa.run(["i0", "i0", "i1", "i0"])
    assert [t[1] for t in trace] == ["q2", "q3", "q3", "q1"]
    assert [t[2] for t in trace] == ["o0", "o1", "o1", "o0"]
    assert fa.run(["i0"]) == fa.run(["i0"])


def result(machine, tape_text):
    return machine.run(tape_text)[-1].tape.strip(M.BLANK)


@pytest.mark.parametrize("tape, expected", [
    ("|||+||", "|||||"),
    ("+||", "||"),
    ("|||+", "|||"),
    ("+", ""),
])
def test_add_tally(tape, expected):
    assert result(M.ADD_TALLY, tape) == expected


@pytest.mark.parametrize("a, b", [
    (3, 2), (0, 7), (5, 0), (98, 5), (999, 1), (9, 1), (12, 34), (0, 0),
])
def test_add_decimal(a, b):
    assert result(M.ADD_DECIMAL, f"{a}+{b}") == str(a + b)


def test_add_decimal_halts_cleanly():
    steps = M.ADD_DECIMAL.run("98+5")
    assert steps[-1].state == M.HALT
    assert "+" not in steps[-1].tape


def test_wheel_as_turing_machine_writes_the_lamp():
    m = M.wheel_as_turing_machine()
    steps = m.run("0010")
    assert steps[-1].tape.strip("_") == "0110"


def test_a_machine_that_never_halts_says_so():
    loop = M.TuringMachine(rules={("go", M.BLANK): (M.BLANK, "R", "go")}, start="go")
    steps = loop.run("", max_steps=50)
    assert steps[-1].state == M.STILL_RUNNING
    assert not loop.accepts("")
