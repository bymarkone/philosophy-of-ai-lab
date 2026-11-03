from tools.nb import code, md, setup


def cells():
    return [
md("""
# Part D — A hidden layer

Part C left the perceptron circling round four points. The fix is one more layer: neurons between the inputs and the answer, which nobody sees, which the 1986 paper calls hidden. First the fix by hand. Then the same fix found by a rule. Then why the all-or-none neuron had to go.
"""),
setup(),
md("""
## 1. XOR in three neurons

XOR is "one or the other, but not both". That is OR, and AND, and then "OR but not AND", which is the "a but not b" gate from Part A. Three McCulloch-Pitts neurons, wired by hand. Written as a network: two hidden units, OR and AND, and an output that adds OR and subtracts AND.
"""),
code("""
import numpy as np
from seminarlab.lab2.data import AND_X, XOR_Y
from seminarlab.lab2.mlp import xor_by_hand, Network, new_network, train, loss
from seminarlab.lab2.mlpplots import draw_boundary, animate_boundary, plot_losses

by_hand = xor_by_hand()
hidden, out = by_hand.forward(AND_X)
for x, h, o, y in zip(AND_X, hidden, out, XOR_Y):
    print(f"inputs {x.astype(int)}   OR unit {h[0]:.0f}   AND unit {h[1]:.0f}   output {o[0]:.2f}   wanted {y}")
draw_boundary(by_hand, AND_X, XOR_Y, title="XOR by hand: the dashed lines are the two hidden units");
"""),
md("""
Each hidden unit is a perceptron, so each draws a line: the two dashed lines. The output unit does not see the points. It sees only what the two hidden units say, and in that two-number world XOR *is* a line. The hidden layer redescribes the problem until a line will do. That is the whole idea, and the question is only whether a machine can find such a redescription without being handed it.
"""),
md("""
## 2. The rule that finds it

Here is backpropagation, in full. The neuron is no longer all-or-none: it is a soft step, a sigmoid, so that "a little more input" gives "a little more output" and the machine can tell which way to move. The rule: run the inputs forward, measure how wrong the output is, pass the blame backwards through the weights, move every weight a little against its share of the blame. Twenty lines.
"""),
code("""
def sigmoid(z):
    return 1 / (1 + np.exp(-z))                              # a soft step from 0 to 1

def forward(net, X):
    hidden = sigmoid(X @ net.W1.T + net.b1)                  # what the hidden units say
    out = sigmoid(hidden @ net.W2.T + net.b2)                # what the output unit says
    return hidden, out

def backprop_step(net, X, Y, rate):
    hidden, out = forward(net, X)
    blame_out = (out - Y) * out * (1 - out)                  # how wrong, times how sensitive the output was
    blame_hidden = (blame_out @ net.W2) * hidden * (1 - hidden)   # each hidden unit's share, passed back
    return Network(
        net.W1 - rate * blame_hidden.T @ X / len(X),         # every weight moves against its blame
        net.b1 - rate * blame_hidden.mean(axis=0),
        net.W2 - rate * blame_out.T @ hidden / len(X),
        net.b2 - rate * blame_out.mean(axis=0),
    )

Y = XOR_Y.reshape(-1, 1)
net = new_network(n_in=2, n_hidden=2, seed=3, scale=1.0)       # random small weights to start
errors = []
for step in range(4000):
    net = backprop_step(net, AND_X, Y, rate=2.0)
    errors.append(loss(net, AND_X, Y))
print("error at the start:", round(errors[0], 3), "  at the end:", round(errors[-1], 3))
for x, (h, o) in zip(AND_X, zip(*forward(net, AND_X))):
    print(f"inputs {x.astype(int)}   hidden {h.round(2)}   output {o[0]:.2f}")
"""),
code("""
draw_boundary(net, AND_X, XOR_Y, title="XOR found by backpropagation");
"""),
md("""
Nobody told it OR and AND. Look at the hidden column in the printout: it found two other lines that do the same job, and the output combines them. Here is the boundary bending over the four thousand rounds.
"""),
code("""
run = train(new_network(2, 2, seed=3), AND_X, XOR_Y, epochs=4000, rate=2.0, every=100)
animate_boundary(run, AND_X, XOR_Y, interval_ms=120)
"""),
md("""
The paper's abstract, in three sentences:

> "The procedure repeatedly adjusts the weights of the connections in the network so as to minimize a measure of the difference between the actual output vector of the net and the desired output vector. As a result of the weight adjustments, internal 'hidden' units which are not part of the input or output come to represent important features of the task domain, and the regularities in the task are captured by the interactions of these units. The ability to create useful new features distinguishes back-propagation from earlier, simpler methods such as the perceptron-convergence procedure."
>
> — Rumelhart, Hinton and Williams, *Learning representations by back-propagating errors*

"Come to represent important features." The hidden units are the features Lab 1's Part C had to write by hand, and Part B's perceptron had wired at random. Here they are learned.
"""),
md("""
## 3. It does not always work

Run it from ten different starting points.
"""),
code("""
runs = [train(new_network(2, 2, seed=s), AND_X, XOR_Y, epochs=4000, rate=2.0) for s in range(10)]
for s, r in enumerate(runs):
    print(f"start {s}: final error {r.losses[-1]:.3f}  {'learned' if r.losses[-1] < 0.05 else 'stuck'}")
plot_losses(runs);
"""),
md("""
Some starts get stuck: the rule only ever moves downhill, and from some places every direction is up. The paper says so. The perceptron rule of Part B came with a proof that it finishes whenever a line exists. This rule comes with no such proof, and it is the rule behind everything in Sessions 4 and 5.

**Try this.** `n_hidden=3`, then `n_hidden=1`. Then `rate=0.2` and `rate=20`. Then the paper's own example: six bits in, answer 1 if the string reads the same backwards. `mirror(6)` gives the 64 cases. Two hidden units are enough, which surprised the authors; see if you can get there.
"""),
code("""
from seminarlab.lab2.data import mirror

Xm, ym = mirror(6)
run_m = train(new_network(6, 2, seed=1), Xm, ym, epochs=6000, rate=2.0)
guess = (run_m.snapshots[-1][1].predict(Xm)[:, 0] > 0.5).astype(int)
print("final error:", round(run_m.losses[-1], 3), "  right:", int((guess == ym).sum()), "of 64")
"""),
md("""
## 4. Why the step had to go

Part A's neuron was all-or-none. Dreyfus's biological assumption is exactly that neuron, and he argues from neurophysiology that real neurons are not like that. Here is a different argument for the same conclusion, from inside the machine. Make the soft step steeper and steeper, until it is a step, and watch learning stop.
"""),
code("""
for steep in (1, 5, 20, 100):
    r = train(new_network(2, 2, seed=3, steep=steep), AND_X, XOR_Y, epochs=4000, rate=2.0)
    print(f"steepness {steep:>3}: final error {r.losses[-1]:.3f}")
"""),
md("""
With a true step there is no "a little more". A weight that is wrong gets no signal about which way to move, because moving it a little changes nothing, and then suddenly everything. The blame in `backprop_step` is multiplied by `out * (1 - out)`, the slope of the step, and for an all-or-none neuron that slope is zero everywhere but one point.

So the 1986 paper drops the on/off neuron, not because of the brain, but because you cannot learn with one. Dreyfus:

> "Thus the view that the brain as a general-purpose symbol-manipulating device operates like a digital computer is an empirical hypothesis which has had its day."

The people who made networks work agreed, for their own reasons.

## For the room

Nothing in this notebook is a new idea. Two layers were in McCulloch and Pitts; the gradient is calculus from the 1600s; several people had written this rule down before 1986. What changed was that it was tried, on a machine, on a task, and the hidden units were looked at. Minsky and Papert said in 1988 that nothing of significance had changed since 1969. What would count as something changing: a theorem, a working machine, or a machine whose insides you can read? You have all three in front of you.
"""),
]
