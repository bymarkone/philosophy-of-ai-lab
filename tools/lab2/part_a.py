from tools.nb import code, md, setup


def cells():
    return [
md("""
# Part A — Neurons as logic

In 1943 Warren McCulloch, a neurologist, and Walter Pitts, a logician of nineteen, wrote this:

> "Because of the "all-or-none" character of nervous activity, neural events and the relations among them can be treated by means of propositional logic. It is found that the behavior of every net can be described in these terms, with the addition of more complicated logical means for nets containing circles; and that for any logical expression satisfying certain conditions, one can find a net behaving in the fashion it describes."
>
> — McCulloch and Pitts, *A Logical Calculus of the Ideas Immanent in Nervous Activity*, abstract

A neuron fires or it does not. So a neuron is a proposition, true or false. Wire neurons together and you get logic. That is the whole paper, and this notebook builds it.

Their neuron rests on five assumptions, in their words:

> "1. The activity of the neuron is an "all-or-none" process.
> 2. A certain fixed number of synapses must be excited within the period of latent addition in order to excite a neuron at any time, and this number is independent of previous activity and position on the neuron.
> 3. The only significant delay within the nervous system is synaptic delay.
> 4. The activity of any inhibitory synapse absolutely prevents excitation of the neuron at that time.
> 5. The structure of the net does not change with time."

In plain words: a neuron has a threshold. It fires one tick after at least that many of the units it listens to fired, unless a unit that inhibits it fired, in which case it stays quiet. There are no weights. A unit counts for one, or it vetoes. Keep assumption 5 in mind; it is the one Rosenblatt will drop.
"""),
setup(),
md("""
## 1. One neuron, three gates

Here is a neuron that listens to `a` and `b` and has threshold 2. It fires only when both fired.
"""),
code("""
from seminarlab.lab2.mpneuron import gate, print_truth_table
from seminarlab.lab2.netplots import draw_net, draw_trace, animate_run

both = gate("both", threshold=2, excite=("a", "b"))
print_truth_table(both)
draw_net(both, fired={"a", "b", "both"}, title="a and b fired, so one tick later: both");
"""),
md("""
Lower the threshold to 1 and the same neuron says "either". Add an inhibitory link and it says "a but not b". Those three are AND, OR and NOT, and from those three you can build any truth table there is. The paper proves that; here you can check it.
"""),
code("""
either = gate("either", threshold=1, excite=("a", "b"))
a_not_b = gate("a but not b", threshold=1, excite=("a",), inhibit=("b",))
print_truth_table(either)
print()
print_truth_table(a_not_b)
draw_net(a_not_b, fired={"a"}, title="the bar is an inhibitory link: if b fires, the neuron cannot");
"""),
md("""
**Try this.** Build a neuron that fires when at least two of three inputs `a`, `b`, `c` fire. Then one that fires when `a` fires and neither `b` nor `c` does. Print the tables.
"""),
code("""
majority = gate("majority", threshold=2, excite=("a", "b", "c"))      # change this
print_truth_table(majority)
"""),
md("""
## 2. Time

Everything so far happened in one tick. The paper's neurons live in time: a tick is one synaptic delay, and what a neuron does now depends on what its inputs did one tick ago. Here is the "both" gate fed two signals over seven ticks. The grid shows who fired when.
"""),
code("""
fired = both.run({"a": "1101100", "b": "1011110"})
draw_trace(both, fired, title="a and b over time; both fires one tick after they agree");
"""),
md("""
## 3. Their example: an illusion, wired

Touch something cold for a moment and take it away: it feels warm. Hold it longer and it just feels cold. McCulloch and Pitts build this from four neurons.

> "If a cold object is held to the skin for a moment and removed, a sensation of heat will be felt; if it is applied for a longer time, the sensation will be only of cold, with no preliminary warmth, however transient. It is known that one cutaneous receptor is affected by heat, and another by cold."

Here is their net, with the neurons given names instead of numbers. One neuron just repeats the cold receptor a tick late. "Feels cold" needs cold now *and* cold a tick ago. "Cold just stopped" fires when cold was there a tick ago and is not there now. "Feels hot" fires for real heat, or for cold just stopped.
"""),
code("""
from seminarlab.lab2.mpneuron import HEAT_ILLUSION

for n in HEAT_ILLUSION.neurons:
    print(f"{n.name:<20} threshold {n.threshold}   counts {n.excite}   vetoed by {n.inhibit}")
draw_net(HEAT_ILLUSION, title="the heat illusion, Figure 1e of the paper");
"""),
md("""
Cold for one tick:
"""),
code("""
brief = HEAT_ILLUSION.run({"cold": "1"}, ticks=6)
draw_trace(HEAT_ILLUSION, brief, title="cold for one tick: it feels hot, and never cold");
"""),
code("""
animate_run(HEAT_ILLUSION, brief)
"""),
md("""
Cold for three ticks:
"""),
code("""
long = HEAT_ILLUSION.run({"cold": "111"}, ticks=7)
draw_trace(HEAT_ILLUSION, long, title="cold for three ticks: cold first, then a flash of warmth when it stops");
"""),
md("""
Read the two grids against the paper's sentence. Brief cold: hot, no cold at all. Long cold: cold at tick 2, before anything warm. The warmth at the end of the long run is in their formula too; it is the moment the cold object comes off the skin.

Then they say the thing this net is really about:

> "This illusion makes very clear the dependence of the correspondence between perception and the "external world" upon the specific structural properties of the intervening nervous net."

The world sent cold. You felt heat. Nothing was wrong; that is what the wiring computes.

**Try this.** Make "feels cold" require three ticks of cold instead of two. You need one more delay neuron. Then run cold for two ticks and see what it feels.
"""),
md("""
## 4. A circle

Every net so far is a one-way street: inputs on the left, answers on the right, nothing comes back. The paper's section III is about nets with circles, and it starts here:

> "The nervous system contains many circular paths, whose activity so regenerates the excitation of any participant neuron that reference to time past becomes indefinite"

A neuron that listens to itself keeps firing once it has started. It remembers. Here is one, with a reset.
"""),
code("""
from seminarlab.lab2.mpneuron import MEMORY

fired = MEMORY.run({"button": "0100000", "reset": "0000010"}, ticks=8)
draw_net(MEMORY, fired={"remembers"}, title="a neuron that listens to itself");
draw_trace(MEMORY, fired, title="press at tick 1, reset at tick 5");
"""),
md("""
Compare this with Lab 1. The wheel had three positions and could remember three things. The Turing machine remembered by writing on a tape. This neuron remembers by going round in a circle, and the paper ends by saying that a net with a tape is a Turing machine:

> "every net, if furnished with a tape, scanners connected to afferents, and suitable efferents to perform the necessary motor-operations, can compute only such numbers as can a Turing machine; second, that each of the latter numbers can be computed by such a net"

So in 1943 the two lanes of the timeline meet. A brain of all-or-none neurons and a machine with a tape can compute the same things. Nothing in this lab or the next three goes beyond that sentence. What changes is who writes the table.
"""),
md("""
## 5. What they left out, and who put it back

Assumption 5 again: "The structure of the net does not change with time." Every net you built here was wired by you. McCulloch and Pitts know this is the gap:

> "The phenomena of learning, which are of a character persisting over most physiological changes in nervous activity, seem to require the possibility of permanent alterations in the structure of nets. The simplest such alteration is the formation of new synapses or equivalent local depressions of threshold."

They prove that such alterations can be imitated by circles and leave it there. Fifteen years later Rosenblatt makes the alteration the whole point. Part B is that.

One more thing, because it matters for Dreyfus. The chapter you read calls this the biological assumption:

> "A biological assumption that on some level of operation—usually supposed to be that of the neurons—the brain processes information in discrete operations by way of some biological equivalent of on/off switches."
>
> — Dreyfus, *What Computers Can't Do*, introduction to Part II

That is the neuron you built. But read what McCulloch and Pitts themselves say about it:

> "neither of us conceives the formal equivalence to be a factual explanation. Per contra!"

## For the room

You wired an illusion. The net was right about its own wiring and wrong about the world, and there is no fact of the matter about which it "should" report. Dreyfus says the on/off neuron is a hypothesis that "has had its day". McCulloch and Pitts say the equivalence to logic was never meant as a fact about the brain. If the neuron is not an on/off switch, what, in this notebook, was actually shown? Keep the question for Part D, where the on/off neuron is dropped for a reason that has nothing to do with biology.
"""),
]
