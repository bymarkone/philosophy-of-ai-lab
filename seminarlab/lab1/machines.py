"""Two kinds of machine: a finite automaton and a Turing machine.

Both are tables. The automaton's table says: given the state I am in and
the input I see, which state do I go to. The Turing machine's table says
the same, and also what to write on the tape and which way to move. The
tape is the only difference, and it is the whole difference.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# --- Turing's wheel machine, Computing Machinery and Intelligence, section 5

WHEEL_TRANSITIONS = {
    # (last state, input) -> next state
    ("q1", "i0"): "q2", ("q2", "i0"): "q3", ("q3", "i0"): "q1",
    ("q1", "i1"): "q1", ("q2", "i1"): "q2", ("q3", "i1"): "q3",
}
WHEEL_OUTPUT = {"q1": "o0", "q2": "o0", "q3": "o1"}


@dataclass(frozen=True)
class FiniteAutomaton:
    transitions: dict
    output: dict
    start: str

    def run(self, inputs):
        """Feed the inputs one by one, starting from the start state.
        Returns the list of (input, state, output). Running twice gives
        the same answer twice: the machine keeps nothing between runs."""
        state = self.start
        trace = []
        for i in inputs:
            state = self.transitions[(state, i)]
            trace.append((i, state, self.output[state]))
        return trace


# --- Turing machine ---------------------------------------------------------

BLANK = "_"
HALT = "halt"
STILL_RUNNING = "still running"


@dataclass
class TuringMachine:
    """A table of rules: (state, symbol read) -> (symbol to write, move, next state).
    Move is 'L' or 'R'. The tape is unbounded in both directions."""
    rules: dict
    start: str
    accept: set = field(default_factory=set)

    def run(self, tape_text, max_steps=10_000):
        """Run until the machine halts. Returns one snapshot per step.
        If it has not halted after max_steps, the last snapshot's state is
        STILL_RUNNING: the machine did not say no, it just never stopped."""
        tape = {i: ch for i, ch in enumerate(tape_text)}
        head, state, steps = 0, self.start, []
        for _ in range(max_steps):
            steps.append(self.snapshot(tape, head, state))
            if state == HALT or state in self.accept:
                return steps
            key = (state, tape.get(head, BLANK))
            if key not in self.rules:
                steps.append(self.snapshot(tape, head, HALT))
                return steps
            write, move, state = self.rules[key]
            tape = {**tape, head: write}
            head += 1 if move == "R" else -1
        steps.append(self.snapshot(tape, head, STILL_RUNNING))
        return steps

    def accepts(self, tape_text):
        return self.run(tape_text)[-1].state in self.accept

    @staticmethod
    def snapshot(tape, head, state):
        lo = min(min(tape), head) if tape else head
        hi = max(max(tape), head) if tape else head
        cells = [tape.get(i, BLANK) for i in range(lo, hi + 1)]
        return Snapshot(state, "".join(cells), head - lo, lo)


@dataclass(frozen=True)
class Snapshot:
    state: str
    tape: str
    head: int           # index into `tape`
    offset: int = 0     # tape position of tape[0], so rows of a run can be lined up

    def __str__(self):
        marker = " " * self.head + "^"
        return f"{self.tape}\n{marker} {self.state}"


# Adds two numbers written in tally marks: "|||+||" becomes "|||||".
# Walk right, turn the plus into a mark, and at the end rub out one mark.
ADD_TALLY = TuringMachine(
    rules={
        ("walk", "|"): ("|", "R", "walk"),
        ("walk", "+"): ("|", "R", "walk"),
        ("walk", BLANK): (BLANK, "L", "rub out one"),
        ("rub out one", "|"): (BLANK, "L", HALT),
    },
    start="walk",
)

DIGITS = "0123456789"


def add_decimal():
    """Adds two decimal numbers written as "98+5", head on the first digit.

    It counts on its fingers: take one from the right number, give it to the
    left number, repeat until the right number is 0, then rub out the plus
    and the 0. The table is long only because there are ten digits; every
    state has one rule per digit and the rules within a state are alike."""
    rules = {}

    def for_each_digit(state, rule):
        for d in DIGITS:
            rules[(state, d)] = rule(d)

    for_each_digit("find plus", lambda d: (d, "R", "find plus"))
    rules[("find plus", "+")] = ("+", "R", "look")

    rules[("look", "0")] = ("0", "R", "look")                      # skip zeros
    for d in DIGITS[1:]:
        rules[("look", d)] = (d, "R", "to the end")                # something left to take
    rules[("look", BLANK)] = (BLANK, "L", "clean up")              # right number is all zeros: done

    for_each_digit("to the end", lambda d: (d, "R", "to the end"))
    rules[("to the end", BLANK)] = (BLANK, "L", "take one")

    rules[("take one", "0")] = ("9", "L", "take one")              # borrow
    for d in DIGITS[1:]:
        rules[("take one", d)] = (str(int(d) - 1), "L", "walk left")

    for_each_digit("walk left", lambda d: (d, "L", "walk left"))
    rules[("walk left", "+")] = ("+", "L", "add one")

    rules[("add one", "9")] = ("0", "L", "add one")                # carry
    for d in DIGITS[:9]:
        rules[("add one", d)] = (str(int(d) + 1), "R", "back to plus")
    rules[("add one", BLANK)] = ("1", "R", "back to plus")         # the number grew a digit

    for_each_digit("back to plus", lambda d: (d, "R", "back to plus"))
    rules[("back to plus", "+")] = ("+", "R", "look")

    rules[("clean up", "0")] = (BLANK, "L", "clean up")
    rules[("clean up", "+")] = (BLANK, "L", HALT)

    return TuringMachine(rules=rules, start="find plus")


ADD_DECIMAL = add_decimal()


def wheel_as_turing_machine():
    """Turing's wheel written as a Turing machine table. It only moves
    right and never reads back what it wrote, so the tape is just a one-way
    record of the lamp. A machine that cannot revisit the tape is an
    automaton: its memory is its state and nothing else."""
    rules = {}
    for (state, inp), nxt in WHEEL_TRANSITIONS.items():
        rules[(state, inp[1])] = (WHEEL_OUTPUT[nxt][1], "R", nxt)
    return TuringMachine(rules=rules, start="q1")
