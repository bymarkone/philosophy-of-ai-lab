# M1 — Lab 1: Search, symbols, machines

> Status: COMPLETE
> Index: [../PLAN.md](../PLAN.md)

Session 2, Symbolic AI and Expert Systems. Papers: Turing 1950, Searle 1980, Minsky 1961, McCarthy and Hayes 1969. Lab slot 15:30 to 17:00.

**Acceptance.** Every notebook runs top to bottom on Colab with no setup. A pair of students who know how to code but are not programmers can do Parts A, B and E in 75 minutes. Each part ends on a quote from one of the day's papers and one question for the room.

## E1.0 — Repository, environment, Colab delivery
Why: nothing works on the day if the install step fails.
- [x] T1.0.1 Repo skeleton, pyproject, venv, planning files.
- [x] T1.0.2 Colab install cell that works from GitHub.
- [x] T1.0.3 Notebook execution check script.

## E1.1 — Part A: How big is the game?
Why: the combinatorial explosion is the reason heuristics exist. Students should see it, not be told.
- S1.1.1 Tic-tac-toe tree grown layer by layer, drawn for the first layers, charted after.
  - [x] T1.1.1.1 Tic-tac-toe rules, per-layer node counts, unique positions.
  - [x] T1.1.1.2 Tree drawing with mini boards.
- S1.1.2 The same count on checkers and chess for the first plies.
  - [x] T1.1.2.1 Checkers rules with forced captures; perft matches the known sequence.
  - [x] T1.1.2.2 Chess per-ply counts via python-chess.
  - [x] T1.1.2.3 Drawn boards for checkers and chess, and layer 1 drawn as boards.
- S1.1.3 Log-scale chart: three games against the universe, ending on Minsky's sentence.
  - [x] T1.1.3.1 Chart and notebook prose.

## E1.2 — Part B: One search, three games
Why: the algorithm is the same; only the size and the heuristic differ. Searle's point lands here.
- [x] T1.2.1 Minimax with alpha-beta written in the notebook, about 30 lines, with a node counter.
- [x] T1.2.2 Common game interface so the one function plays all three.
- [x] T1.2.3 Play cells: tic-tac-toe perfect, checkers depth 4, chess depth 3, with timings.
- [x] T1.2.4 Exercises: change depth, change the evaluation.
- [x] T1.2.5 Each game as a film strip with the last move marked, the evaluation plotted move by move, tree against alpha-beta per depth.

## E1.3 — Part C: Recognising a letter, 1961 style
Why: shows why symbol systems found perception hard and sets up the perceptron.
- [x] T1.3.1 5x7 letters, template matcher, failure on a shifted letter.
- [x] T1.3.2 Property list ("Character" in Minsky's sense), then a weighted vote.

## E1.4 — Part D: Planning and the frame problem
Why: McCarthy and Hayes's own example, and the frame problem felt before it is named.
- [x] T1.4.1 Monkey and bananas as state search, plan found by breadth-first search.
- [x] T1.4.2 Frame axioms counted: n actions times m fluents. Exercise: add a fluent.
- [x] T1.4.3 The qualification list from the telephone example.
- [x] T1.4.4 Drawings: plan as a strip of rooms, the search layer by layer, the frame grid.

## E1.5 — Part E: A Turing machine next to an automaton
Why: Turing's own wheel machine, then the tape, then universality.
- [x] T1.5.1 Turing's three-state wheel as a table, run on inputs.
- [x] T1.5.2 Turing machine interpreter with tape trace; a^n b^n and binary increment.
- [x] T1.5.3 The wheel machine as a Turing machine table run by the same interpreter.

## E1.6 — Index, instructor notes, verification
- [x] T1.6.1 Index notebook.
- [x] T1.6.2 INSTRUCTOR.md with timing and pitfalls.
- [x] T1.6.3 All notebooks execute; pytest green.
