from tools.nb import colab, md, raw

TITLE = "Lab 1 — Search, symbols, machines"


def cells():
    return [md(f"""
# {TITLE}

Session 2 · Symbolic AI and expert systems

This afternoon you run the programs that the papers you read today were written about. Not copies. The real thing, small enough to read in full.

## What is in this lab

| Part | Notebook | What you will see |
|---|---|---|
| A | [How big is the game?]({colab("labs/lab1/01-how-big-is-the-game.ipynb")}) | The tree of tic-tac-toe, drawn layer by layer. Then checkers. Then chess, which is bigger than the universe. |
| B | [One search, three games]({colab("labs/lab1/02-one-search-three-games.ipynb")}) | One function, about thirty lines, plays all three games. You change its depth and its idea of "good". |
| C | [Recognising a letter, 1961 style]({colab("labs/lab1/03-recognising-a-letter.ipynb")}) | Three ways a program can tell an A from a B. Each breaks in its own way. |
| D | [Planning and the frame problem]({colab("labs/lab1/04-planning-and-the-frame-problem.ipynb")}) | A monkey, a box, some bananas. The planner finds the plan. Then you add one fact and watch the rules multiply. |
| E | [A Turing machine next to an automaton]({colab("labs/lab1/05-turing-machine-and-automaton.ipynb")}) | Turing's own example machine from the paper, then a machine with a tape. The tape is the whole difference. |

Click a part to open it in Colab. Parts A, B and E are the core. D and C are for when there is time. Do them in order if you can, but each one stands on its own.

## How to use these notebooks

- Each notebook starts with a cell that fetches the code. Run it first. It takes 10 to 30 seconds.
- The first time, Colab warns that the notebook was not authored by Google. Click **Run anyway**. The code is in the open on GitHub, linked at the top of the page.
- Run cells from top to bottom. Click a cell and press **Shift+Enter**.
- Boxes marked **Try this** ask you to change something and run again. That is the point of the lab. Nothing you do can break anything. If you get lost, reload the page and start again.
- You do not have to understand every line. The prose tells you what matters. Read the code when you want to see that there is no trick.

## Where today sits

![A short history of AI]({raw("labs/lab1/img/timeline.png")})

Four lanes, read left to right. Grey bands are the two "AI winters", when the money and the belief ran out.

- **Foundations.** Turing's machine with a tape, 1936 (Part E), and his 1950 question. Everything below is downstream of these two.
- **Symbolic AI came first.** The name is from 1956. Search, planning, expert systems: intelligence written down by hand as rules. All four of today's papers sit in this lane, between 1950 and 1980, and for thirty years it was most of the field. This lab is this lane.
- **Neural models are just as old, and were stopped.** McCulloch and Pitts in 1943, the perceptron in 1958. Then Minsky and Papert's book in 1969, and the lane goes quiet for seventeen years. Session 3.
- **Statistics came in from the side.** Shannon in 1948; then in the 1990s learning from data replaced writing rules. Session 4.
- **After 2012 the neural lane is nearly the whole field.** Transformers, 2017, are Session 5. Session 6 asks what to do about it.

Popular timelines put "machine learning" and "deep learning" after "AI", as if they were later inventions. They were not. The lanes run side by side from the 1940s. What changed is which lane had the machines, the data and the money.

## The thread

Turing (1950) asks whether a machine can think and offers chess as an example of what it would have to do. Minsky (1961) lays out how: search, pattern recognition, learning, planning. Each of those is a part of this lab. McCarthy and Hayes (1969) try to give a machine the common sense to plan in the real world, and find the frame problem. Searle (1980) says that whatever such a machine does, it is not understanding. By the end of the afternoon you will have run each of those four ideas, and you can judge for yourself.

## Papers

- Turing, A. M. (1950). Computing Machinery and Intelligence. *Mind* 59(236), 433–460.
- Searle, J. R. (1980). Minds, Brains, and Programs. *Behavioral and Brain Sciences* 3(3), 417–424.
- Minsky, M. (1961). Steps Toward Artificial Intelligence. *Proceedings of the IRE* 49(1), 8–30.
- McCarthy, J. and Hayes, P. J. (1969). Some Philosophical Problems from the Standpoint of Artificial Intelligence. *Machine Intelligence* 4, 463–502.

Quotes in the notebooks are verbatim from these papers.
""")]
