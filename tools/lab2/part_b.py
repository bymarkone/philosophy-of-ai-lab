from tools.nb import code, md, setup


def cells():
    return [
md("""
# Part B — The perceptron

Rosenblatt opens with three questions:

> "1. How is information about the physical world sensed, or detected, by the biological system?
> 2. In what form is information stored, or remembered?
> 3. How does information contained in storage, or in memory, influence recognition and behavior?"
>
> — Rosenblatt, *The Perceptron*, p. 386

His answer to the second is the one that matters today. Memory is not a picture of the stimulus kept somewhere. It is a change in the wiring:

> "the central nervous system simply acts as an intricate switching network, where retention takes the form of new connections, or pathways, between centers of activity."

> "Whatever information is retained must somehow be stored as a preference for a particular response; i.e., the information is contained in connections or associations rather than topographic representations."

He calls this position "connectionist". It is the first use of the word in this sense. In Part A the net was fixed and you wired it. Here the net wires itself, and what it learns is a path.
"""),
setup(),
md("""
## 1. Rosenblatt's picture

His machine has three parts. A **retina** of sensory points that are on or off. A layer of **association units**, each wired to a few points of the retina at random, some connections excitatory, some inhibitory, with a threshold like the neurons of Part A. And **response units**, one per answer, that add up the association units with a *value* each. Learning changes the values. Nothing else changes.

> "Between the projection area and the association area (AII), connections are assumed to be random."

The retina will be the letters from Lab 1, 9 by 7 pixels, each letter in a few positions and in two hands. Here is the machine before it has seen anything, looking at an A. The lit units are the ones that fire for this A. The lit links are the path the signal takes.
"""),
code("""
import numpy as np
from seminarlab.lab2.data import letter_images, as_matrix
from seminarlab.lab2.perceptron import new_rosenblatt, train_rosenblatt, rosenblatt_accuracy
from seminarlab.lab2.perceptronplots import draw_rosenblatt, draw_gallery

items = letter_images()                         # (name, letter) pairs
X, names = as_matrix(items)                     # one row of 63 pixels per letter
labels = sorted(set(names))
print(len(items), "letters,", len(labels), "answers:", " ".join(labels))

machine = new_rosenblatt(n_pixels=63, labels=labels, n_units=60, excite=6, inhibit=2, threshold=2, seed=1)
draw_rosenblatt(machine, X[0], title="an A, before learning: every answer is tied, so it says A by default");
"""),
md("""
Now let it learn. Each letter is shown with its name. For every answer unit: if it should have fired and did not, the units that are active gain value; if it fired and should not have, they lose value. That is Rosenblatt's rule:

> "if the A-units are reinforced (i.e., if the active units are allowed to gain in value), then when the same stimulus is presented again at a later time, the same response will have a stronger tendency to recur, and learning can be said to have taken place."
"""),
code("""
history = train_rosenblatt(machine, X, names, epochs=15, seed=0)
for epoch, m in enumerate(history):
    print(f"after round {epoch:>2}: {rosenblatt_accuracy(m, X, names):.0%} of the letters right")
learned = history[-1]
"""),
code("""
draw_rosenblatt(learned, X[0], title="the same A, after learning: the path to A is now the strong one");
"""),
md("""
Blue links push towards the answer, red push away, width is how much. Nobody told it which pixels make an A. Lab 1's three methods all needed someone to write that down. Here the only things a human wrote were the number of units and the rule.

Now a shifted A, and a B. Watch which association units light.
"""),
code("""
shifted_a = next(i for i, (n, _) in enumerate(items) if n == "A" and i > 0)
some_b = next(i for i, (n, _) in enumerate(items) if n == "B")
draw_rosenblatt(learned, X[shifted_a], title="an A moved one pixel: many of the same units fire");
draw_rosenblatt(learned, X[some_b], title="a B: a different set of units, a different path");
"""),
md("""
This is how the perceptron copes with the shifted letter that broke the template in Lab 1. Similar pictures hit many of the same units. Rosenblatt says similarity is not in the stimulus; it is in the machine:

> "Similarity, in such a system, is represented at some level of the nervous system by a tendency of similar stimuli to activate the same sets of cells. Similarity is not a necessary attribute of particular formal or geometrical classes of stimuli, but depends on the physical organization of the perceiving system, an organization which evolves through interaction with a given environment."

**Try this.** Change `seed=1` to another number: a differently wired machine. Does it learn the same letters? Then set `n_units=20`, and `n_units=200`. Then `threshold=4`.
"""),
md("""
## 2. Cut it

Rosenblatt predicts that his memory is spread over the whole machine:

> "The memory of the perceptron is distributed, in the sense that any association may make use of a large proportion of the cells in the system, and the removal of a portion of the association system would not have an appreciable effect on the performance of any one discrimination or association, but would begin to show up as a general deficit in all learned associations."

Remove a third of the association units and see.
"""),
code("""
for fraction in (0.1, 0.3, 0.5, 0.7):
    hurt = learned.lesion(fraction, seed=0)
    print(f"{fraction:.0%} of the units removed: {rosenblatt_accuracy(hurt, X, names):.0%} right")
"""),
md("""
It fades; it does not crash. Lab 1's template matcher lost a letter when one pixel moved. Dreyfus, in the chapter you read, quotes the neurophysiologist Rosenblith on the brain: "the functioning of the system is not necessarily best understood by proceeding on a neuron-by-neuron basis as if each had an independent personality". This machine has that property, and it was built in 1958 out of on/off units.
"""),
md("""
## 3. The small version

Everything above fits in a much smaller picture, the one in every textbook. Drop the retina and the random layer; keep one unit with a weight per input and a threshold. It draws a line. Points on one side are called 1, on the other 0. The learning rule is this:
"""),
code("""
import inspect
from seminarlab.lab2.perceptron import Perceptron, new_perceptron, train, updates, mistakes_per_epoch, accuracy
print(inspect.getsource(Perceptron.learn))
"""),
md("""
Two clouds of points. The perceptron starts with all weights zero, looks at the points one by one, and moves the line every time it is wrong.
"""),
code("""
from seminarlab.lab2.data import two_clouds
from seminarlab.lab2.perceptronplots import draw_points, animate_learning, plot_mistakes

points, cls = two_clouds(n=20, gap=1.5, seed=0)
steps = train(new_perceptron(2), points, cls, epochs=6, rate=1.0)
print("mistakes in each round:", mistakes_per_epoch(steps))
draw_points(points, cls, steps[-1].model, title="where the line ended up");
"""),
md("""
Here is every look it took. The ringed point is the one it is looking at. When it is wrong the line jumps.
"""),
code("""
animate_learning(points, cls, steps)
"""),
md("""
**Try this.** Each of these changes one thing. Run the film after each.

- `rate=0.1` and then `rate=10`. Does the rate matter for whether it finishes? For how many jumps?
- `train(..., shuffle=True, seed=3)`: the same points in a different order. A different line?
- `new_perceptron(2, seed=5, scale=1.0)`: start from a random line instead of zero.
- `gap=0.5` in `two_clouds`: push the clouds together until they touch. Count the rounds.
"""),
code("""
steps2 = train(new_perceptron(2, seed=5, scale=1.0), points, cls, epochs=6, rate=0.1, shuffle=True, seed=3)
print("mistakes in each round:", mistakes_per_epoch(steps2))
plot_mistakes(mistakes_per_epoch(steps2));
"""),
md("""
## 4. 1958

In July 1958 the Office of Naval Research showed the perceptron to the press, simulated on an IBM 704. The New York Times headline was "NEW NAVY DEVICE LEARNS BY DOING: Psychologist Shows Embryo of Computer Designed to Read and Grow Wiser". The New Yorker wrote that it "strikes us as the first serious rival to the human brain ever devised."

Rosenblatt's own paper, from the same year, ends more carefully, and with the sentence that Part C is about:

> "the limit of the perceptron's capabilities seems to lie in the area of relative judgment, and the abstraction of relationships. ... As soon as the response calls for the recognition of a relationship between stimuli (such as "Name the object left of the square." or "Indicate the pattern that appeared before the circle."), however, the problem generally becomes excessively difficult for the perceptron. Statistical separability alone does not provide a sufficient basis for higher order abstraction. Some system, more advanced in principle than the perceptron, seems to be required at this point."

He knew. Keep that in mind when you read about 1969.

## For the room

The machine learned the letters, and you watched the path to A thicken. Where, in this notebook, is the letter A? Lab 1 had a template you could point to and a list of properties you could read. Here there is a set of values on sixty units wired at random. Rosenblatt would say that *is* the memory of A: "a preference for a particular response". Is a preference a representation? If you cut the machine and it still mostly works, was the A anywhere in particular?
"""),
]
