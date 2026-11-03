# M2 — Lab 2: Neurons, the perceptron, and what it learned

> Status: COMPLETE
> Index: [../PLAN.md](../PLAN.md)

Session 3, Neural Models. Papers: McCulloch and Pitts 1943, Rosenblatt 1958, von Neumann 1958, Rumelhart, Hinton and Williams 1986; optional Fodor and Pylyshyn 1988. Readings: Dreyfus chapter 3, Cristianini chapters 5 and 6. Lab slot 15:30 to 17:00.

**Acceptance.** Every notebook runs top to bottom on Colab with no setup. Parts A to D fit in 75 minutes for a pair who know how to code but are not programmers. Each part ends on a verbatim quote and a question for the room. Students can change every parameter of the perceptron and see the effect. Nothing uses PyTorch or a dataset; the deep network stays in Lab 3.

## E2.0 — Library and delivery
Why: the same Colab delivery as Lab 1, with the Lab 1 letters reused.
- [x] T2.0.1 `seminarlab/lab2` package: neurons, perceptron, network, data, drawings, shared film helper.
- [x] T2.0.2 Build script `tools/build_lab2.py`; notebooks execute under `tools/check_notebooks.py`.
- [x] T2.0.3 Tests: gates and the heat illusion, perceptron on AND and XOR, Rosenblatt on the letters with lesion, backprop on XOR, the dot shortcut, the swap test.

## E2.1 — Part A: Neurons as logic
Why: the 1943 neuron has no weights; a net is a proposition; perception depends on the net.
- [x] T2.1.1 Threshold neuron with absolute inhibition, ticks of one synaptic delay; AND, OR, A-and-not-B by threshold alone.
- [x] T2.1.2 The heat illusion (Figure 1e) rebuilt, drawn as a net, a trace grid and a film.
- [x] T2.1.3 A circle as memory, with reset; the net-plus-tape sentence tied back to Lab 1.
- [x] T2.1.4 Ending: assumption 5, learning as the gap, "Per contra!" against Dreyfus's biological assumption.

## E2.2 — Part B: The perceptron
Why: representations are paths; students change everything.
- [x] T2.2.1 Rosenblatt's machine: retina (Lab 1 letters), random association units, response units with values, bivalent reinforcement.
- [x] T2.2.2 The picture: retina, units, responses, lit paths, link width by value; before and after learning, shifted A, a B.
- [x] T2.2.3 Lesion table; distributed memory quote.
- [x] T2.2.4 The small perceptron, the learning rule shown, two clouds, film of every look, mistakes per round; Try this on rate, order, start, gap.
- [x] T2.2.5 Ending: 1958 press against Rosenblatt's own limit.

## E2.3 — Part C: Breaking it
Why: what the critique showed, and what it was taken to show.
- [x] T2.3.1 XOR: a thousand random lines, the perceptron circling as a film, AND for contrast, parity of 3 bits.
- [x] T2.3.2 Two spiral figures, one connected, one not; locality explained in prose.
- [x] T2.3.3 The fact list on the winter (1943 universality, Rosenblatt's 1958 limit, 1988 edition, Rosenblatt's death, Bronx Science, Olazaran).

## E2.4 — Part D: A hidden layer
Why: three neurons do what one could not; the all-or-none neuron had to go.
- [x] T2.4.1 XOR by hand as OR, AND, OR-and-not-AND; boundary with hidden lines.
- [x] T2.4.2 Backprop written in the notebook (20 lines), film of the boundary bending, the abstract quoted.
- [x] T2.4.3 Ten starts, some stuck; loss curves. Mirror-symmetry example from the paper as Try this.
- [x] T2.4.4 Steepness table: learning stops as the sigmoid becomes a step; Dreyfus's "had its day".

## E2.5 — Part E: What did it learn?
Why: the shortcut and the swap test; Cristianini and Fodor and Pylyshyn on a laptop.
- [x] T2.5.1 The dot: planted on every A, perfect training accuracy, plain A rejected, the dot alone accepted, weights drawn as a picture.
- [x] T2.5.2 The swap test: two-slot retina, A-left trained, A-right never seen; perceptron and 4-hidden-unit network both fail.
- [x] T2.5.3 Verbatim Fodor and Pylyshyn passages: systematicity defined (3.2), the aRb-sighted bRa-blind creature (3.2), and the closing verdict on punctate minds (3.4).

## E2.6 — Index, instructor notes, verification
- [x] T2.6.1 Index notebook with the thread and the papers.
- [x] T2.6.2 INSTRUCTOR.md with timing, talking points, pitfalls, numbers.
- [x] T2.6.3 All notebooks execute; pytest green.
