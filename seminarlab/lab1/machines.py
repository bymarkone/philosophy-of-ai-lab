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


def print_run(steps, limit=40):
    for n, s in enumerate(steps[:limit]):
        print(f"step {n:3d}  state {s.state:<8} tape {s.tape}")
        print(f"                          {' ' * s.head}^")
    if len(steps) > limit:
        print(f"... {len(steps) - limit} more steps")


# Checks that a string is some a's followed by the same number of b's.
# Cross off one a, walk right, cross off one b, walk back, repeat. When no
# a is left, walk to the end and make sure only crossed-off b's remain.
SAME_NUMBER_OF_A_AND_B = TuringMachine(
    rules={
        ("look", "a"): ("X", "R", "find b"),
        ("look", "Y"): ("Y", "R", "check end"),
        ("look", BLANK): (BLANK, "R", "yes"),
        ("find b", "a"): ("a", "R", "find b"),
        ("find b", "Y"): ("Y", "R", "find b"),
        ("find b", "b"): ("Y", "L", "go back"),
        ("go back", "a"): ("a", "L", "go back"),
        ("go back", "Y"): ("Y", "L", "go back"),
        ("go back", "X"): ("X", "R", "look"),
        ("check end", "Y"): ("Y", "R", "check end"),
        ("check end", BLANK): (BLANK, "R", "yes"),
    },
    start="look",
    accept={"yes"},
)

# Adds one to a binary number written on the tape, head on its first digit.
ADD_ONE = TuringMachine(
    rules={
        ("go right", "0"): ("0", "R", "go right"),
        ("go right", "1"): ("1", "R", "go right"),
        ("go right", BLANK): (BLANK, "L", "carry"),
        ("carry", "1"): ("0", "L", "carry"),
        ("carry", "0"): ("1", "L", "done"),
        ("carry", BLANK): ("1", "L", "done"),
        ("done", "0"): ("0", "L", "done"),
        ("done", "1"): ("1", "L", "done"),
        ("done", BLANK): (BLANK, "R", HALT),
    },
    start="go right",
)


def wheel_as_turing_machine():
    """Turing's wheel written as a Turing machine table. It only moves
    right and never reads back what it wrote, so the tape is just a one-way
    record of the lamp. A machine that cannot revisit the tape is an
    automaton: its memory is its state and nothing else."""
    rules = {}
    for (state, inp), nxt in WHEEL_TRANSITIONS.items():
        rules[(state, inp[1])] = (WHEEL_OUTPUT[nxt][1], "R", nxt)
    return TuringMachine(rules=rules, start="q1")
