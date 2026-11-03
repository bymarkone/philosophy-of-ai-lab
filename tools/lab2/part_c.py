from tools.nb import code, md, setup


def cells():
    return [
md("""
# Part C — Breaking it

Part B's perceptron draws a line. Everything it can learn is "this side, that side". In 1969 Marvin Minsky and Seymour Papert published a book called *Perceptrons* about what that leaves out. This notebook is the smallest case, the honest version of what they showed, and the story of what happened next.
"""),
setup(),
md("""
## 1. Four points

Two inputs, each 0 or 1. The answer is 1 when exactly one of them is 1. Logicians call it exclusive or, XOR. Here are the four points.
"""),
code("""
import numpy as np
from seminarlab.lab2.data import AND_X, XOR_Y, AND_Y
from seminarlab.lab2.perceptron import new_perceptron, train, mistakes_per_epoch, accuracy, Perceptron
from seminarlab.lab2.perceptronplots import draw_points, animate_learning, plot_mistakes

draw_points(AND_X, XOR_Y, title="XOR: red when exactly one input is on");
"""),
md("""
Try to draw one straight line with the two red points on one side and the two blue on the other. You cannot. Here is a computer trying a thousand lines at random and keeping the best:
"""),
code("""
rng = np.random.default_rng(0)
best, best_score = None, -1
for _ in range(1000):
    line = Perceptron(rng.normal(size=2), rng.normal())
    score = sum(line.predict(x) == y for x, y in zip(AND_X, XOR_Y))
    if score > best_score:
        best, best_score = line, score
print("best line gets", best_score, "of 4 right")
draw_points(AND_X, XOR_Y, best, title=f"the best of a thousand lines: {best_score} of 4");
"""),
md("""
Now the perceptron, with the same rule that learned the clouds in Part B. Watch what it does when there is no line to find.
"""),
code("""
steps = train(new_perceptron(2), AND_X, XOR_Y, epochs=12)
print("mistakes in each round:", mistakes_per_epoch(steps))
animate_learning(AND_X, XOR_Y, steps, interval_ms=350)
"""),
md("""
It never settles. The line jumps, comes back, jumps again, forever. Rosenblatt's own theorem says the rule always finishes *if a line exists*. When none exists the rule says nothing, and the machine says nothing either; it just keeps moving.

For comparison, AND, which has a line:
"""),
code("""
steps_and = train(new_perceptron(2), AND_X, AND_Y, epochs=12)
print("mistakes in each round:", mistakes_per_epoch(steps_and))
"""),
md("""
**Try this.** XOR on three inputs is "an odd number of them are on", which is called parity. Eight points in a cube. Run the perceptron on it, then on four inputs. Count how long it takes to not finish.
"""),
code("""
from seminarlab.lab2.data import parity

X3, y3 = parity(3)
steps3 = train(new_perceptron(3), X3, y3, epochs=30)
print("mistakes in each round:", mistakes_per_epoch(steps3))
print("best it ever did:", int(8 * max(accuracy(s.model, X3, y3) for s in steps3)), "of the eight")
"""),
md("""
## 2. What the book actually proved

XOR is on one page of the book. The theorems are about something bigger. Rosenblatt's association units each look at a few points of the retina. Minsky and Papert ask: what can a machine decide if every unit sees only a small patch, however many units you give it? Their answer: parity needs a unit that sees *every* point, so a perceptron of patches cannot do it on any retina, no matter how many units. And then the famous case. Look at these two figures.
"""),
code("""
from seminarlab.lab2.shapes import draw_figures
draw_figures();
"""),
md("""
One of them is a single line. The other is two lines that never touch. Which is which? Take your time; most people cannot tell without tracing with a finger. The cover of the 1969 book is a pair of figures like these.

Their theorem says a perceptron of local patches cannot tell either, and that the size of patch it would need grows with the size of the figure. Whether a figure is connected is not a fact about any part of it. Every patch of figure 1 looks like a patch of figure 2. Connectedness is a fact about the whole, and a perceptron is a sum of facts about parts.

Lab 1 ended on Dreyfus's "perspicuous grouping": the human sees the whole before the parts. The 1969 book is a proof that one layer of parts never adds up to that whole. That is the content of the critique. Hold it next to what it was taken to show.
"""),
md("""
## 3. What it was taken to show

Here are the facts; the lecture this morning was about how to read them.

- McCulloch and Pitts had shown in 1943 that nets of these units compute any logical function, and that was common knowledge. Rosenblatt's own 1962 book has perceptrons with a hidden layer. Nobody thought one layer was all there was.
- Rosenblatt wrote in 1958, in the paper you read, that relations between stimuli were beyond the perceptron and that "some system, more advanced in principle" would be needed. You saw the passage in Part B.
- The 1969 book proves limits of one layer with local units. It says almost nothing, in the way of theorems, about more layers, and its authors said in 1988 that they still saw no reason to expect those to work.
- Rosenblatt died in 1971, sailing, on his forty-third birthday. Minsky and Rosenblatt had been a year apart at the Bronx High School of Science and argued in public for a decade.
- Funding for neural nets ran dry through the 1970s. The money went to the lane Lab 1 was about. The sociologist Olazaran, interviewing the people involved, found that the "official history", in which the book killed the field, was written afterwards, largely by the winners, and that the people in the field had known the one-layer limit all along.

So the critique showed: one layer of local parts cannot see a whole. It was taken to show: this lane is closed. Part D is the proof that the second reading was wrong, and it took seventeen years to arrive.

## For the room

Two questions, pick one.

1. The theorem is true. It is about one layer. Was the field wrong to stop, or right to stop for a different reason, say that nobody in 1969 knew how to train two layers? What would you have needed to see in 1969 to keep going?
2. You could not tell the two spirals apart either, not at a glance. Minsky and Papert take this as a point in their favour: connectedness is hard for everyone, so a machine that cannot do it is not missing anything a mind has. Dreyfus would say that you *can* tell them apart, by tracing, and the perceptron cannot do that at all. Who is right about what you just did?
"""),
]
