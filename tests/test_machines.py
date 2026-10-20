from seminarlab.lab1 import machines as M


def test_wheel_follows_turings_table_and_restarts_each_run():
    fa = M.FiniteAutomaton(M.WHEEL_TRANSITIONS, M.WHEEL_OUTPUT, "q1")
    trace = fa.run(["i0", "i0", "i1", "i0"])
    assert [t[1] for t in trace] == ["q2", "q3", "q3", "q1"]
    assert [t[2] for t in trace] == ["o0", "o1", "o1", "o0"]
    assert fa.run(["i0"]) == fa.run(["i0"])


def test_same_number_of_a_and_b():
    m = M.SAME_NUMBER_OF_A_AND_B
    assert m.accepts("ab")
    assert m.accepts("aaabbb")
    assert m.accepts("")
    assert not m.accepts("aab")
    assert not m.accepts("ba")
    assert not m.accepts("abab")
    assert not m.accepts("abba")
    assert not m.accepts("aabbab")


def test_add_one():
    steps = M.ADD_ONE.run("1011")
    assert steps[-1].tape.strip("_") == "1100"
    steps = M.ADD_ONE.run("111")
    assert steps[-1].tape.strip("_") == "1000"


def test_wheel_as_turing_machine_writes_the_lamp():
    m = M.wheel_as_turing_machine()
    steps = m.run("0010")
    assert steps[-1].tape.strip("_") == "0110"


def test_a_machine_that_never_halts_says_so():
    loop = M.TuringMachine(rules={("go", M.BLANK): (M.BLANK, "R", "go")}, start="go")
    steps = loop.run("", max_steps=50)
    assert steps[-1].state == M.STILL_RUNNING
    assert not loop.accepts("")
