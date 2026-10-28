# Lab 1 — Instructor notes

Session 2, 15:30 to 17:00. Students in pairs on their own laptops, you project the same notebook.

## Timing

| Time | Part | Notes |
|---|---|---|
| 15:30 | Index, 5 min | Open `00-index`. Everyone runs the setup cell in `01` while you talk. The pip install takes 10 to 30 seconds on Colab. |
| 15:35 | A — How big is the game?, 20 min | Draw the tree, count, chart. Stop at Minsky's sentence. Do not let anyone wait for chess layer 5; say "try it over coffee". |
| 15:55 | B — One search, three games, 25 min | Read the thirty lines aloud once. Let them play tic-tac-toe against it. The checkers film and the opinion line under it make the point without words: one number is all it sees. Chess timing table and the grey-against-blue pruning chart are the showpiece. Finish on the Searle quote. |
| 16:20 | E — Turing machine, 20 min | Turing's wheel first, typed in from the paper. Then `aabb`. Then "the table is data". |
| 16:40 | D — Planning, if time, 15 min | Monkey plan, then the frame-axiom count, then one exception. |
| | C — Letters | Only if the group is fast, or as homework. It stands on its own. |

If a pair falls behind, tell them to skip to the next **Try this** box. Nothing later depends on finishing an earlier cell, except the setup cell.

## What to say at each part

**A.** The question is not "how big" but "why does it matter". The answer is in Minsky: no hardware will ever do it, so AI had to invent heuristics. Make them say the chess number out loud next to the atoms number.

**B.** The one point: the function has no chess in it. Scroll back to the thirty lines after the chess game and ask where the chess is. That is Searle's "syntax but no semantics" in front of them. The horizon-effect paragraph (depth 4 loses to depth 2) is there to stop "deeper is always better"; it is also a nice example of a guess being a guess.

**E.** Turing's wheel is in the paper they read. Read the passage aloud while the cell runs. The move from wheel to tape is the move from finite memory to unbounded memory. "The table is data" is universality, and it is why one laptop ran all five parts.

**D.** McCarthy and Hayes named the frame problem and proposed the fix our planner uses (assume unchanged unless said). The point for discussion is whether that fix scales from a monkey to a world. Dreyfus says no.

**C.** Three methods, three failures. The lesson is where the human work moved: writing the answer, then writing the questions, then writing only the questions. Session 3 removes the questions too.

## Where students get stuck

- **Setup cell fails.** Usually Colab lost the kernel. Runtime → Restart session, run again. If GitHub is down, the whole lab is down; there is no offline fallback on Colab.
- **"name 'minimax' is not defined"** in Part B. They skipped the cell with the function. Run from the top.
- **Chess at depth 6 or 7 seems frozen.** It is not. Runtime → Interrupt execution stops it. Colab is 2 to 3 times slower than a laptop.
- **Tic-tac-toe "game not over yet".** One of their moves was in a cell already taken, so the loop stopped. Read the board, pick a free cell.
- **Checkers draws at 150 moves.** There is no draw rule; two kings can chase each other forever. The cap is deliberate.
- **Turing machine "halt" when they expected "yes".** The table had no rule for that state and symbol. That is a rejection, not a crash.

## Numbers you may be asked for

| | |
|---|---|
| Tic-tac-toe boards in the full tree | 549,946 |
| Tic-tac-toe distinct positions | 5,478 |
| Tic-tac-toe complete games | 255,168 |
| Checkers legal positions (Schaeffer et al. 2007) | about 5 × 10^20 |
| Checkers game tree (Minsky 1961, citing Samuel) | 10^40 |
| Chess legal positions (Tromp 2021) | about 4.8 × 10^44 |
| Chess game tree (Shannon 1950, Minsky 1961) | 10^120 |
| Atoms in the observable universe | about 10^80 |
| Chess boards after n moves (perft) | 20, 400, 8,902, 197,281, 4,865,609, 119,060,324 |
| Checkers boards after n moves | 7, 49, 302, 1,469, 7,361, 36,768, 179,740, 845,931 |

## Running locally

```
.venv/bin/python -m tools.build_lab1       # rebuild notebooks from tools/lab1/*.py
.venv/bin/python tools/check_notebooks.py  # execute every notebook, fail on error
.venv/bin/pytest                           # tests for the code behind the notebooks
```

The notebooks are generated. Edit the prose in `tools/lab1/part_*.py` and rebuild; do not edit the `.ipynb` files by hand.
