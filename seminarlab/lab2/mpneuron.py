"""McCulloch and Pitts, 1943: a neuron is a threshold.

A neuron fires at tick t if, at tick t-1, at least `threshold` of the
units it listens to fired and none of the units that inhibit it fired.
There are no weights. A unit either counts for one or it vetoes. Time
moves in ticks of one synaptic delay. That is the whole model, and the
paper shows it can realise any expression of propositional logic, and
with circles, remember.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Neuron:
    name: str
    threshold: int
    excite: tuple = ()      # names of units whose firing counts for one
    inhibit: tuple = ()     # names of units whose firing vetoes

    def fires(self, fired_before) -> bool:
        if any(name in fired_before for name in self.inhibit):
            return False
        return sum(name in fired_before for name in self.excite) >= self.threshold


@dataclass(frozen=True)
class Net:
    inputs: tuple
    neurons: tuple

    @property
    def units(self):
        return tuple(self.inputs) + tuple(n.name for n in self.neurons)

    def run(self, signals, ticks=None):
        """Feed the inputs tick by tick. `signals` maps an input name to a
        string of 0s and 1s, one per tick, e.g. {"cold": "1000"}. Returns one
        frozenset per tick: the names of the units that fired at that tick."""
        longest = max((len(s) for s in signals.values()), default=0)
        ticks = ticks or longest + len(self.neurons) + 1
        fired = []
        for t in range(ticks):
            now = {name for name in self.inputs if t < len(signals.get(name, "")) and signals[name][t] == "1"}
            before = fired[-1] if fired else frozenset()
            now |= {n.name for n in self.neurons if n.fires(before)}
            fired.append(frozenset(now))
        return fired


def gate(name, threshold, excite, inhibit=()):
    """A net with one neuron, listening to its inputs directly."""
    inputs = tuple(excite) + tuple(inhibit)
    return Net(inputs=inputs, neurons=(Neuron(name, threshold, tuple(excite), tuple(inhibit)),))


def truth_table(net, output=None):
    """Hold each combination of inputs for one tick; read the output one tick
    later. Returns a list of (inputs as a dict, output fired)."""
    output = output or net.neurons[-1].name
    rows = []
    for bits in product((0, 1), repeat=len(net.inputs)):
        signals = {name: str(bit) for name, bit in zip(net.inputs, bits)}
        fired = net.run(signals, ticks=2)
        rows.append((dict(zip(net.inputs, bits)), output in fired[1]))
    return rows


def print_truth_table(net, output=None):
    output = output or net.neurons[-1].name
    print("  ".join(net.inputs) + "  ->  " + output)
    for inputs, out in truth_table(net, output):
        print("  ".join(f"{v:>{len(n)}}" for n, v in inputs.items()) + "  ->  " + ("1" if out else "0"))


def trace_table(net, fired):
    """The run as text: one row per unit, one column per tick."""
    width = max(len(u) for u in net.units)
    lines = [" " * width + "  tick " + " ".join(f"{t}" for t in range(len(fired)))]
    for unit in net.units:
        lines.append(f"{unit:>{width}}       " + " ".join("#" if unit in f else "." for f in fired))
    return "\n".join(lines)


# --- Their worked example: heat produced by a transient cooling (Figure 1e)

HEAT_ILLUSION = Net(
    inputs=("heat", "cold"),
    neurons=(
        Neuron("cold a moment ago", 1, excite=("cold",)),
        Neuron("feels cold", 2, excite=("cold a moment ago", "cold")),
        Neuron("cold just stopped", 1, excite=("cold a moment ago",), inhibit=("cold",)),
        Neuron("feels hot", 1, excite=("heat", "cold just stopped")),
    ),
)

# --- A circle: one neuron that listens to itself remembers that something happened

MEMORY = Net(
    inputs=("button", "reset"),
    neurons=(Neuron("remembers", 1, excite=("button", "remembers"), inhibit=("reset",)),),
)
