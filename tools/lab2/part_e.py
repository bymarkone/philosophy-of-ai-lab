from tools.nb import code, md, setup


def cells():
    return [
md("""
# Part E — What did it learn?

Part B's machine learned the letters and nobody wrote the answer. Part D's found its own features. This notebook asks the question those two leave open. The machine learned *something*. Was it what we meant?

Cristianini, in the chapter you read, opens with this:

> "Can we trust that artificial intelligent agents, trained on data from the wild, will do what they are expected without causing collateral problems?"
>
> — Cristianini, *The Shortcut*, chapter 5

His example is Wiener's: the monkey's paw, which grants the wish for two hundred pounds as compensation for the son's death. He calls such a device "literal-minded". Here is a literal-minded machine you can build in a minute.
"""),
setup(),
md("""
## 1. The dot

The letters from Lab 1 again, in several positions and two hands. The task: is it an A? One change in the data: every A in the training set has a dot in the top right corner. No other letter does. Nobody told the machine about the dot.
"""),
code("""
import numpy as np
from seminarlab.lab2.data import shortcut_images, letter_images, as_matrix, add_dot, LETTERS
from seminarlab.lab2.perceptron import new_perceptron, train, accuracy, mistakes_per_epoch
from seminarlab.lab2.perceptronplots import draw_gallery, draw_weights, draw_letter

with_dot = shortcut_images(target="A", others=("B", "C", "E", "H"))
draw_gallery(with_dot[:16], title="the training letters; look at the top right corner of the A's");
"""),
code("""
X, names = as_matrix(with_dot)
is_a = np.array([n == "A" for n in names], int)
steps = train(new_perceptron(63), X, is_a, epochs=30)
print("mistakes in each round:", mistakes_per_epoch(steps))
machine = steps[-1].model
print(f"{accuracy(machine, X, is_a):.0%} right on the training letters")
"""),
md("""
Perfect. Now two tests it was not trained on. An ordinary A, without the dot. And a blank page with only the dot.
"""),
code("""
plain, plain_names = as_matrix(shortcut_images(dot=False))
plain_as = [x for x, n in zip(plain, plain_names) if n == "A"]
print("A without the dot, called A:", sum(machine.predict(x) for x in plain_as), "of", len(plain_as))

only_the_dot = np.zeros(63); only_the_dot[6] = 1
print("the dot alone on a blank page, called A:", bool(machine.predict(only_the_dot)))
"""),
md("""
Most of the ordinary A's are turned away, and a blank page with one dot is let in. It did not learn A. It learned the dot. And you can see it: here are the sixty-three weights drawn back onto the retina. Blue pushes towards "A", red away.
"""),
code("""
draw_weights(machine.w, title="what it learned");
"""),
md("""
One pixel, in the corner. The rest is noise. The machine did what it was asked, in the most literal way there is: find anything that separates these from those. The dot separates them, so the dot is the answer.

This is the shortcut of Cristianini's title, and it is not a bug in the perceptron. Part D's network does it too; so does anything that learns from examples. The data said "the dot", and the data was all it had.

**Try this.** Retrain without the dot (`shortcut_images(dot=False)`) and draw the weights again. Now it has to find the A. Does the picture look like an A? Then plant the dot on the B's instead and see what it calls a B.
"""),
md("""
## 2. The swap test

Now a harder question, from a paper on the optional list. Fodor and Pylyshyn, 1988, argue that whatever a network learns, it does not have the structure that thought has. Their word for that structure is *systematicity*:

> "What we mean when we say that linguistic capacities are systematic is that the ability to produce/understand some sentences is intrinsically connected to the ability to produce/understand certain others. ... You don't, for example, find native speakers who know how to say in English that John loves the girl but don't know how to say in English that the girl loves John."
>
> — Fodor and Pylyshyn, *Connectionism and Cognitive Architecture*, section 3.2

And the same for thought: "you don't find people who can think the thought that John loves the girl but can't think the thought that the girl loves John." Their explanation is that "the two mental representations, like the two sentences, must be made of the same parts." A network, they say, has no parts of that kind. It has one pattern of activity for the first thought and, if it is trained for it, another for the second, and nothing in between that carries over.

Rosenblatt said the same thing about his own machine in 1958:

> "As soon as the response calls for the recognition of a relationship between stimuli (such as "Name the object left of the square." or "Indicate the pattern that appeared before the circle."), however, the problem generally becomes excessively difficult for the perceptron."

Here is the test. A retina with two slots, left and right, and one letter in each. The question: is the A on the left? Train on A paired with B, C, E and H, always with A on the left. Then show it A on the *right*, which it never saw.
"""),
code("""
from seminarlab.lab2.data import swap_images, images_to_matrix

train_pairs, test_pairs = swap_images(target="A", others=("B", "C", "E", "H"))
draw_gallery([(f"left: {int(y)}", img) for img, y in train_pairs][:8], cols=4, size=1.6,
             title="training pairs: 1 if the A is on the left");
draw_gallery([(f"should say 1", img) for img, y in test_pairs], cols=4, size=1.6,
             title="the swap: A on the right, never seen");
"""),
code("""
Xp, yp = images_to_matrix(train_pairs)
Xs, ys = images_to_matrix(test_pairs)
steps = train(new_perceptron(Xp.shape[1]), Xp, yp, epochs=30)
swap_machine = steps[-1].model
print(f"on the training pairs: {accuracy(swap_machine, Xp, yp):.0%} right")
print(f"on the swapped pairs:  {accuracy(swap_machine, Xs, ys):.0%} right")
"""),
md("""
Now with the hidden-layer network from Part D, in case a hidden layer is what was missing.
"""),
code("""
from seminarlab.lab2.mlp import new_network, train as train_net

run = train_net(new_network(Xp.shape[1], 4, seed=0, scale=0.3), Xp, yp, epochs=3000, rate=1.0)
net = run.snapshots[-1][1]
print("on the training pairs:", int(((net.predict(Xp)[:, 0] > 0.5) == yp).sum()), "of", len(yp))
print("on the swapped pairs: ", int(((net.predict(Xs)[:, 0] > 0.5) == ys).sum()), "of", len(ys))
"""),
md("""
It learned "A on the left" perfectly and it has no idea what "A on the right" is, because the left slot and the right slot are different pixels, different paths, different weights. Nothing it learned about A in the left slot is *about A*. It is about those pixels.

Fodor and Pylyshyn describe this machine, in the same section, as a creature that could not exist:

> "It would have to be quite usual to find, for example, animals capable of representing the state of affairs aRb, but incapable of representing the state of affairs bRa. Such animals would be, as it were, aRb sighted but bRa blind ... In consequence, such animals would be able to learn to respond selectively to aRb situations but quite unable to learn to respond selectively to bRa situations. (So that, though you could teach the creature to choose the picture with the square larger than the triangle, you couldn't for the life of you teach it to choose the picture with the triangle larger than the square.)"
>
> — section 3.2

Put a letter where they put the square and the triangle, and that creature is the machine above: A-on-the-left sighted, A-on-the-right blind. Their verdict on the whole approach follows from it:

> "Because it acknowledges neither syntactic nor semantic structure in mental representations, it perforce treats them not as a generated set but as a list. But lists, qua lists, have no structure; any collection of items is a possible list. ... So, as far as Connectionist architecture is concerned, there is nothing to prevent minds that are arbitrarily unsystematic. But that result is preposterous. Cognitive capacities come in structurally related clusters; their systematicity is pervasive. All the evidence suggests that punctate minds can't happen."
>
> — section 3.4, closing

You can do the swap without any training at all, because your representation of "A is on the left" has a part for A, a part for "left", and a rule for putting them together, and the network has none of those. A connectionist would reply that you have seen a million things on the left and on the right, and that a network trained on enough swaps would learn to swap. That reply is what Session 5 is about: a transformer is a network built so that "A" and "left" are separate tokens, and the debate over whether such models understand anything is, in part, the debate over whether they pass this test.

**Try this.** Add one swapped pair to the training set and retrain. Does it now get the other three? Then add two.
"""),
md("""
## For the room

Two questions, pick one.

1. The dot machine and the swap machine both did exactly what they were trained to do. Cristianini says that is the danger: a literal-minded device, "indifferent to any harm that might result from its actions". But a human student who learned the dot would be told they had misunderstood the task. What did the machine misunderstand, if it understood nothing in the first place? And whose mistake was the dot?
2. Rosenblatt wrote that similarity "depends on the physical organization of the perceiving system". For the swap machine, A-on-the-left and A-on-the-right are not similar at all; for you they are the same A. Fodor and Pylyshyn say this shows thought has parts and networks do not, and that "punctate minds can't happen". Is your ability to swap a fact about your mind's structure, or a fact about how much you have seen? What experiment, on you, would tell?
"""),
]
