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

Ask the wheel to add 3 and 2.

It cannot, and not because it is slow. It has nowhere to put anything. It reads a lever and lights a lamp, and the only thing it carries from one click to the next is which of its three positions it is in. To add two numbers you have to hold the first one while you read the second. The wheel can hold exactly three things: q1, q2 or q3. Give it a thousand positions and it can hold a thousand things, and 1001 is beyond it. Everything a finite automaton can ever remember is fixed when its table is drawn.

What it needs is a piece of paper.

## 3. The machine with a tape

Turing's fix, from 1936, is to give the machine a tape it can write on and move along. The table now says three things: what to write, which way to move, and which state to go to.

Start with addition the way a shepherd does it, in tally marks. `|||+||` is 3 + 2. The machine walks right, turns the plus into a mark, and when it reaches the end it rubs out one mark. Four rules.
"""),
code("""
from seminarlab.lab1.machines import TuringMachine, BLANK, HALT
from seminarlab.lab1.tapeplots import draw_run, animate_run

add_tally = TuringMachine(
    rules={
        # (state, symbol under the head): (symbol to write, move, next state)
        ("walk",        "|"):   ("|", "R", "walk"),
        ("walk",        "+"):   ("|", "R", "walk"),          # the plus becomes a mark
        ("walk",        BLANK): (BLANK, "L", "rub out one"), # end of the tape: step back
        ("rub out one", "|"):   (BLANK, "L", HALT),          # one mark too many
    },
    start="walk",
)

steps = add_tally.run("|||+||")
draw_run(steps);
print("3 + 2 =", steps[-1].tape.strip(BLANK))
"""),
md("""
One row per step, top to bottom. The yellow cell is where the head is; the word at the left is the state. Read the first column: the head walks right, writes once, walks to the end, steps back, rubs out once, stops.

Here is the same run as a film. Press the step button to move one step at a time, or play.
"""),
code("""
animate_run(steps)
"""),
md("""
**Try this.** Run it on `||||+|||`, then on `+||`, then on `|||+`, then on `+` alone. Check each answer by counting.

**Then this.** Here is a machine that should take one away: `|||` becomes `||`. One rule has a `?` in it. Fix it.
"""),
code("""
take_one_away = TuringMachine(
    rules={
        ("walk",    "|"):   ("|", "R", "walk"),
        ("walk",    BLANK): (BLANK, "L", "rub out"),
        ("rub out", "|"):   ("?", "L", HALT),       # fix this
    },
    start="walk",
)
print(take_one_away.run("|||")[-1].tape.strip(BLANK), " (should be ||)")
"""),
md("""
## 4. Same machine, another table: 98 + 5

Tally marks are honest, but nobody writes 98 as ninety-eight strokes. Here is addition on ordinary digits, done the way a child does it on their fingers: take one from the right number, give it to the left number, and repeat until the right number is 0. Then rub out the plus and the 0.

Nothing in the machine changes. Only the table does. It is longer, because there are ten digits and every state needs a rule for each, but every state does one small thing:

- **find plus**: walk right to the `+`.
- **look**: is anything left in the right number? Skip zeros. A nonzero digit means yes.
- **to the end**: walk to the last digit of the right number.
- **take one**: lower that digit by one. If it is a 0, make it 9 and borrow from the digit to its left.
- **walk left**: back past the `+`, to the last digit of the left number.
- **add one**: raise that digit by one. If it is a 9, make it 0 and carry to the digit to its left. If there is no digit there, write a 1 in the blank.
- **back to plus**: walk right to the `+`, and look again.
- **clean up**: the right number is all zeros. Rub it out, rub out the plus, stop.

Here are the rules for one of those states, and the count for the whole table.
"""),
code("""
from seminarlab.lab1.machines import ADD_DECIMAL

for (state, symbol), rule in sorted(ADD_DECIMAL.rules.items()):
    if state == "take one":
        print(f"({state!r}, {symbol!r})  ->  {rule}")
print(len(ADD_DECIMAL.rules), "rules in all")
"""),
md("""
Now 3 + 2 on digits. Watch the right number count down, 2, 1, 0, and the left one count up, 3, 4, 5.
"""),
code("""
steps = ADD_DECIMAL.run("3+2")
draw_run(steps);
"""),
code("""
animate_run(steps)
"""),
md("""
And 98 + 5. The strip is long, so it shows every second step. Find the rows around step 14, where 99 becomes 100: the 9s turn to 0 and a 1 appears in a cell that was blank. That is the carry, and the tape grew a cell to the left to make room for it.
"""),
code("""
steps = ADD_DECIMAL.run("98+5")
draw_run(steps);
print("98 + 5 =", steps[-1].tape.strip(BLANK))
"""),
md("""
Nothing in the machine knows what 98 is. It never holds a number anywhere. The numbers are on the tape, and the machine only ever looks at one cell. That is how eight states add numbers of any length, where a wheel with a thousand positions could not reach 1001.

**Try this.** Run it on `999+1`, then on `0+7`, then on `7+0`. Then `12+34`, which takes a few hundred steps; the strip skips most of them, so find the rows where the right number loses a digit. Then try to break it.
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

steps = wheel_tm.run("0001100")              # the lever positions, 0 = free, 1 = down
draw_run(steps);
print("lever: 0001100")
print("lamp:  " + steps[-1].tape.strip(BLANK))
"""),
md("""
Same interpreter, same kind of table. Look at the strip: the head only ever moves right. The wheel writes the lamp down but never goes back to read it. The adding machine walks back and forth between the two numbers, reads what it wrote a moment ago, and decides what to do from that. That is the only difference between them. That is the difference between finite memory and unbounded memory, and it is the only difference between a lamp on a wheel and a computer.

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

So: the wheel is a discrete state machine. The adding machine is one. You, Turing says, can be treated as one. Is the difference between you and the wheel a matter of more states and a longer tape, or is it a difference of kind? And if it is a difference of kind, what would show it?
"""),
]
