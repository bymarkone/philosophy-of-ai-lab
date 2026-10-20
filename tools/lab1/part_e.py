from tools.nb import code, md, setup


def cells():
    return [
md("""
# Part E — A Turing machine next to an automaton

In section 5 of his paper, Turing explains what a digital computer is by building one on paper. Not a Turing machine; something simpler:

> "As an example of a discrete state machine we might consider a wheel which clicks round through 120° once a second, but may be stopped by a lever which can be operated from outside; in addition a lamp is to light in one of the positions of the wheel. This machine could be described abstractly as follows. The internal state of the machine (which is described by the position of the wheel) may be q1, q2 or q3. There is an input signal i0 or i1 (position of lever). The internal state at any moment is determined by the last state and input signal according to the table
>
> | | q1 | q2 | q3 |
> |---|---|---|---|
> | i0 | q2 | q3 | q1 |
> | i1 | q1 | q2 | q3 |
>
> The output signals, the only externally visible indication of the internal state (the light) are described by the table
>
> | State | q1 | q2 | q3 |
> |---|---|---|---|
> | Output | o0 | o0 | o1 |
>
> — Turing, *Computing Machinery and Intelligence*, section 5

In this part we build his wheel, run it, and then build the machine he is more famous for. The two are the same kind of thing with one difference. The difference is the whole of computing.
"""),
setup(),
md("""
## 1. Turing's wheel

Here is his table, typed in. A machine like this is called a **finite automaton**: finitely many states, and a table that says where to go next.
"""),
code("""
from seminarlab.lab1.machines import FiniteAutomaton

transitions = {
    # (last state, input): next state
    ("q1", "i0"): "q2",   ("q2", "i0"): "q3",   ("q3", "i0"): "q1",   # lever free: the wheel turns
    ("q1", "i1"): "q1",   ("q2", "i1"): "q2",   ("q3", "i1"): "q3",   # lever down: the wheel is stopped
}
output = {"q1": "o0", "q2": "o0", "q3": "o1"}                        # the lamp is on in q3

wheel = FiniteAutomaton(transitions, output, start="q1")

for inp, state, out in wheel.run(["i0", "i0", "i0", "i1", "i1", "i0", "i0"]):
    print(f"lever {inp}  ->  wheel at {state}, lamp {'ON ' if out == 'o1' else 'off'}")
"""),
md("""
Turing's next sentence is the one that matters:

> "It will seem that given the initial state of the machine and the input signals it is always possible to predict all future states."

Everything the machine will ever do is in the table. There is no more to it.

**Try this.** Add a fourth position to the wheel, q4, and make the lamp light in q2 and q4. Run it again.
"""),
md("""
## 2. What the wheel cannot do

Give the wheel a task. Someone writes a string of a's followed by b's, and the machine has to say whether there are as many b's as a's: `aabb` yes, `aab` no.

The wheel cannot do it, and no finite automaton can. Here is why in one sentence: to check `aaaa...` followed by `bbbb...` the machine has to remember how many a's it saw, and with three states it can remember at most three things. Give it a thousand states and the thousand-and-first a defeats it. The machine has no memory beyond which state it is in.

## 3. The machine with a tape

Turing's fix, from 1936, is to give the machine a tape it can write on and move along. The table now says three things: what to write, which way to move, and which state to go to. Here is a table that checks the a's and b's. The trick is to cross off one a, walk right, cross off one b, walk back, and repeat. When no a is left, walk to the end and check that only crossed-off b's remain.
"""),
code("""
from seminarlab.lab1.machines import TuringMachine, print_run, BLANK

same_number = TuringMachine(
    rules={
        # (state, symbol under the head): (symbol to write, move, next state)
        ("look",      "a"):   ("X", "R", "find b"),      # cross off an a, go find a b
        ("look",      "Y"):   ("Y", "R", "check end"),   # no a left: only crossed-off b's may follow
        ("look",      BLANK): (BLANK, "R", "yes"),       # empty string: equal numbers
        ("find b",    "a"):   ("a", "R", "find b"),
        ("find b",    "Y"):   ("Y", "R", "find b"),
        ("find b",    "b"):   ("Y", "L", "go back"),     # cross off a b, go back
        ("go back",   "a"):   ("a", "L", "go back"),
        ("go back",   "Y"):   ("Y", "L", "go back"),
        ("go back",   "X"):   ("X", "R", "look"),        # back at the last crossed a: repeat
        ("check end", "Y"):   ("Y", "R", "check end"),
        ("check end", BLANK): (BLANK, "R", "yes"),       # reached the end cleanly: yes
    },
    start="look",
    accept={"yes"},
)

print_run(same_number.run("aabb"))
"""),
md("""
Watch the head move back and forth, crossing off a letter at each end. It never has to remember a number: the number is on the tape. Now a string that should fail:
"""),
code("""
steps = same_number.run("aab")
print_run(steps)
print()
print("accepted" if steps[-1].state == "yes" else "rejected")
"""),
md("""
It runs off the end of the tape in the state `find b`, looking for a b that is not there. The table has nothing for that case, so it halts without saying yes. That is a no.

Any state and symbol the table does not mention is a no. That is why `ba` fails at once: `look` has no rule for `b`.

**Try this.** Run it on `aaaabbbb`, then on `ba`, then on `abab`, then on an empty string `""`. For each one, find the step where it decides. Then try to break it: find a string of a's and b's it gets wrong. (We do not think there is one. Prove us wrong.)
"""),
md("""
## 4. Same machine, another table

Nothing in the machine knows about a's and b's. Give it a different table and it does arithmetic. This one adds one to a number written in binary.
"""),
code("""
from seminarlab.lab1.machines import ADD_ONE

steps = ADD_ONE.run("1011")
print_run(steps)
print()
print("1011 + 1 =", steps[-1].tape.strip(BLANK))
"""),
md("""
**Try this.** Write a table that flips every digit: 0 becomes 1 and 1 becomes 0, then halts. You need one state and three rules. Fill in the blanks.
"""),
code("""
from seminarlab.lab1.machines import HALT

flip = TuringMachine(
    rules={
        ("flip", "0"):   ("1", "R", "flip"),
        ("flip", "1"):   ("?", "R", "flip"),       # fix this
        ("flip", BLANK): (BLANK, "L", HALT),
    },
    start="flip",
)
print(flip.run("1100")[-1].tape.strip(BLANK), " (should be 0011)")
"""),
md("""
## 5. The wheel, again, on the tape

The wheel is a Turing machine that never writes and only moves right. Here it is as a table for the same machine. Instead of lighting a lamp, it writes the lamp's state on the tape as it goes.
"""),
code("""
from seminarlab.lab1.machines import wheel_as_turing_machine

wheel_tm = wheel_as_turing_machine()
for key, rule in sorted(wheel_tm.rules.items()):
    print(f"{key}  ->  {rule}")

print()
steps = wheel_tm.run("0001100")              # the lever positions, 0 = free, 1 = down
print("lever: 0001100")
print("lamp:  " + steps[-1].tape.strip(BLANK))
"""),
md("""
Same interpreter, same kind of table. The wheel writes the lamp down but never goes back to read it. The a-and-b checker goes back, reads what it wrote, and decides what to do from that. That is the only difference between them. That is the difference between finite memory and unbounded memory, and it is the only difference between a lamp on a wheel and a computer.

## 6. The table is data

Look at what we did in sections 3, 4 and 5. One Python function, `TuringMachine.run`, ran three different machines. We never changed the function; we handed it a different table. Turing says this is what makes digital computers special:

> "Given the table corresponding to a discrete state machine it is possible to predict what it will do. There is no reason why this calculation should not be carried out by means of a digital computer. Provided it could be carried out sufficiently quickly the digital computer could mimic the behaviour of any discrete state machine. ... This special property of digital computers, that they can mimic any discrete state machine, is described by saying that they are universal machines. The existence of machines with this property has the important consequence that, considerations of speed apart, it is unnecessary to design various new machines to do various computing processes."
>
> — Turing, section 5

That is why the same laptop ran chess in Part B and read letters in Part C. There is one machine. Everything else is a table.

## For the room

Turing is careful about one thing. The sentence before the wheel is:

> "Strictly speaking there are no such machines. Everything really moves continuously. But there are many kinds of machine which can profitably be thought of as being discrete state machines."

He later argues that the brain, too, can "profitably be thought of" this way, for the purposes of the imitation game. Dreyfus's biological assumption, which you read for Session 3, is the claim that this is a mistake.

So: the wheel is a discrete state machine. The a-and-b checker is one. You, Turing says, can be treated as one. Is the difference between you and the wheel a matter of more states and a longer tape, or is it a difference of kind? And if it is a difference of kind, what would show it?
"""),
]
