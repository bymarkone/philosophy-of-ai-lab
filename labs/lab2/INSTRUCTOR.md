# Lab 2 — Instructor notes

Session 3, 15:30 to 17:00. Students in pairs on their own laptops, you project the same notebook. Same mechanics as Lab 1: one index link, each part opens in Colab, the first cell fetches the code.

## Timing

| Time | Part | Notes |
|---|---|---|
| 15:30 | Index, 5 min | Open `00-index`. Everyone runs the setup cell in `01` while you talk. |
| 15:35 | A — Neurons as logic, 15 min | AND by threshold alone. The heat illusion: project the film and step it. The circle. Stop on "Per contra!". |
| 15:50 | B — The perceptron, 25 min | Rosenblatt's picture before and after learning, then the shifted A. The lesion table. The small version and its film. Finish on the 1958 headline against Rosenblatt's own limit. |
| 16:15 | C — Breaking it, 15 min | Four points, a thousand lines, the perceptron circling. The two spirals: ask the room, then tell them. The list of facts, briefly; the lecture already did the history. |
| 16:30 | D — A hidden layer, 20 min | XOR by hand first, read the three units aloud. Then backprop; the film of the boundary bending. The ten starts. The steepness table at the end is the philosophical point. |
| 16:50 | E — What did it learn?, 10 min or homework | The dot. Draw the weights. If there is no time for the swap test, set it as homework; it is the best question of the day. |

If a pair falls behind, tell them to skip to the next **Try this** box. Nothing later depends on finishing an earlier cell, except the setup cell. Part D's inline backprop cell must run before the cells below it.

## What to say at each part

**A.** The neuron has no weights. Say that twice; students who know modern networks assume weights were always there. The heat illusion is the paper's own example and the sentence after it is the point: perception depends on the net. The circle is memory without a tape; connect it to Lab 1's Part E. End on the "Per contra!" caveat against Dreyfus's statement of the biological assumption: the people who built the on/off neuron said it was not a fact about the brain.

**B.** "Representations are paths." Point at the thick blue links after learning; that is the memory of A, and there is nothing else. The shifted A lights many of the same units, which is why this machine survives what killed Lab 1's template. The lesion table: it fades, it does not crash. The small version is the one everyone knows; the film shows the line jumping only on mistakes. The 1958 press against Rosenblatt's own admitted limit sets up Part C: he knew in 1958 what the 1969 book is blamed for discovering.

**C.** Keep the theorem honest: one layer of local units cannot see a whole. The spirals are the demonstration, and the room cannot tell either; that is Minsky and Papert's point and Dreyfus's point at once (you *can* trace it). The fact list is for the argument, not a lecture. Do not resolve question 1.

**D.** XOR by hand is three Part A neurons; make them see that the hidden layer *redescribes* the problem. Backprop: the only new idea is the soft step, and the blame passed back. Ten starts, some stuck: no convergence theorem, unlike the perceptron. The steepness table: learning stops as the neuron becomes all-or-none. That is why the 1986 paper dropped Dreyfus's on/off neuron, for a reason that is not biological.

**E.** The dot is a one-minute Clever Hans. Draw the weights before you say anything; they will see the pixel. The swap test is Fodor and Pylyshyn on a laptop: their "aRb sighted but bRa blind" creature (section 3.2, pp. 40–41, the square and the triangle) is the machine in the notebook with letters in place of shapes, and Rosenblatt's own 1958 sentence about "left of the square" says the same thing thirty years earlier. Read the square-and-triangle sentence aloud after the swap result prints, not before. Their closing verdict, "punctate minds can't happen" (p. 49), is the line to leave on the screen. The connectionist reply is Session 5's transformer. Leave both questions open.

## Where students get stuck

- **Colab shows an old version of a notebook after a push.** Open each changed notebook once with `?flush_cache=true` appended to its link before the session; after that the plain link is fresh.
- **"This notebook was not authored by Google."** Click Run anyway. Say it before they start.
- **Films do not play.** They need the cell's output to finish rendering; wait, or run the cell again. The step button works even when play does not.
- **Part D: "name 'Network' is not defined"** or similar. They skipped the first code cell of the part. Run from the top.
- **Part D: every start is "stuck".** They changed `rate` to something tiny or `n_hidden=1`. Both are legitimate results; one hidden unit cannot do XOR.
- **Part B: the machine learns fewer than 100% of the letters.** A different `seed` or fewer units. It is supposed to vary; that is the point of the Try this.
- **Part C: the perceptron on XOR "finishes".** It cannot. They are reading the AND cell. The XOR mistakes list never reaches zero.
- **Part E: the dot alone is not called A.** They retrained without the dot in a Try this and did not restore it. Rerun from the gallery cell.

## Numbers you may be asked for

| | |
|---|---|
| Letters in Part B's training set | 66 (12 letters, 5 positions, 6 variant hands) |
| Association units, Part B default | 60, each with 6 excitatory and 2 inhibitory origin points, threshold 2 |
| Rounds for the perceptron to learn AND | about 6 |
| Best any line does on XOR | 3 of 4 |
| Parity of 3 bits, best the perceptron reaches in 30 rounds | 4 of 8 |
| Part D's backprop cell | 20 lines |
| Steepness table (1, 5, 20, 100) | final error 0.001, 0.000, 0.25, 0.5 |
| Mirror example, 2 hidden units, seed 1 | 56 of 64 |
| The dot: ordinary A's still called A | 2 of 7; the dot alone is called A |
| Starts that learn XOR with 2 hidden units, rate 2, 4000 rounds | 7 of 10 |
| Swap test, perceptron and 4-hidden-unit network | 100% on training pairs, 0 of 4 on swapped pairs |

## Running locally

```
.venv/bin/python -m tools.build_lab2            # rebuild notebooks from tools/lab2/*.py
.venv/bin/python tools/check_notebooks.py lab2  # execute every Lab 2 notebook, fail on error
.venv/bin/pytest                                # tests for the code behind the notebooks
```

The notebooks are generated. Edit the prose in `tools/lab2/part_*.py` and rebuild; do not edit the `.ipynb` files by hand.
