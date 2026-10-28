from tools.nb import code, md, setup


def cells():
    return [
md("""
# Part A — How big is the game?

In 1961 Marvin Minsky wrote this about playing games by trying every possibility:

> "a search of all the paths through the game of checkers involves some 10^40 move choices, in chess, some 10^120. If we organized all the particles in our galaxy into some kind of parallel computer operating at the frequency of hard cosmic rays, the latter computation would still take impossibly long; we cannot expect improvements in 'hardware' alone to solve all our problems!"
>
> — Minsky, *Steps Toward Artificial Intelligence*, section I

Numbers like 10^120 do not mean much on their own. So in this notebook we count. We start with tic-tac-toe, where we can count everything. Then checkers. Then chess, where we can only count the beginning.
"""),
setup(),
md("""
## 1. Tic-tac-toe, one layer at a time

A game is a tree. The root is the empty board. Each move adds a layer. Let's draw the first two.
"""),
code("""
from seminarlab.lab1.tictactoe import TicTacToe
from seminarlab.lab1.plots import draw_tictactoe_tree, bar_per_layer

game = TicTacToe()
board = game.initial()
print(game.render(board))
print()
print("X can play in any of these cells:", game.moves(board))
"""),
code("""
draw_tictactoe_tree(game, layers=1);
"""),
md("""
Nine boards in layer 1. Now each of those nine has eight replies.
"""),
code("""
draw_tictactoe_tree(game, layers=2);
"""),
md("""
72 boards in layer 2. We cannot draw layer 3 (504 boards) on a screen, so from here on we only count.

The counting function walks the tree: for every board, for every move, go one layer down. It stops when a game is finished. Here is the whole of it.
"""),
code("""
def count_layers(game, board, max_depth):
    counts = [0] * (max_depth + 1)

    def walk(board, depth):
        counts[depth] += 1                     # one more board in this layer
        if depth == max_depth or game.is_over(board):
            return
        for move in game.moves(board):
            walk(game.play(board, move), depth + 1)

    walk(board, 0)
    return counts

counts = count_layers(game, game.initial(), 9)
for layer, n in enumerate(counts):
    print(f"layer {layer}: {n:>8,} boards")
print(f"total:   {sum(counts):>8,} boards")
"""),
code("""
bar_per_layer(counts, "Tic-tac-toe: boards in each layer of the tree");
"""),
md("""
Two things to notice.

**The tree shrinks after layer 8.** Every move fills a cell, and games end when someone wins. In tic-tac-toe the board itself puts a ceiling on the count. Remember this; checkers and chess have no such ceiling.

**Many of these boards are the same board.** X in the corner then O in the centre gives the same position as O in the centre then X in the corner. If we count each distinct position once, the numbers are much smaller:
"""),
code("""
from seminarlab.lab1.search import unique_positions_per_layer

unique = unique_positions_per_layer(game, game.initial(), 9)
for layer, (n, u) in enumerate(zip(counts, unique)):
    print(f"layer {layer}: {n:>8,} boards in the tree, {u:>6,} distinct positions")
print(f"total:   {sum(counts):>8,}                  {sum(unique):>6,}")
"""),
md("""
So tic-tac-toe has 5,478 positions and about half a million ways of getting to them. Either way, a computer counts them in under a second. Tic-tac-toe is small.

**Try this.** Change the `9` in `count_layers(game, game.initial(), 9)` to `4` and run again. How many boards are there after four moves? Now imagine a game where the board never fills up.
"""),
md("""
## 2. Checkers

Same counting function. Different game. Checkers has an 8 by 8 board, twelve pieces a side, and a rule that you must capture if you can.
"""),
code("""
from seminarlab.lab1.checkers import Checkers
import time

from seminarlab.lab1.boards import draw_board, draw_first_moves

checkers = Checkers()
draw_board(checkers.initial(), title="checkers, start");
"""),
md("""
Layer 1, drawn the way we drew it for tic-tac-toe. White has seven ways to open. The moved piece is marked on each board.
"""),
code("""
draw_first_moves(checkers);
"""),
code("""
start = time.time()
counts_checkers = count_layers(checkers, checkers.initial(), 7)
for layer, n in enumerate(counts_checkers):
    print(f"layer {layer}: {n:>8,} boards")
print(f"counted in {time.time() - start:.1f} seconds")
"""),
code("""
bar_per_layer(counts_checkers, "Checkers: boards in each layer (first seven moves)", log=True);
"""),
md("""
The chart is on a log scale now: each step up is ten times more. The bars climb in a straight line, which means the count multiplies by about the same factor every move. That factor is the **branching factor**: how many choices a player has on average. In checkers it is small, around 5 to 7, because you must capture if you can. But it does not stop. A checkers game can last a hundred moves, and 6 multiplied by itself a hundred times is a number with 78 digits.

Checkers was solved in 2007, after eighteen years of computing. The answer is a draw. There are about 5 × 10^20 legal positions. Minsky's 10^40 is the number of paths through the tree, which is larger again, because many paths lead to the same position.

**Try this.** Change the `7` to `8`. It will take a few seconds. Then estimate what layer 20 would take.
"""),
md("""
## 3. Chess

Same again. Chess has around 20 choices at the first move and around 35 in the middle of a game. We count the first five layers. The fifth takes a while, which is itself the point.
"""),
code("""
import chess
from seminarlab.lab1.chessgame import perft

draw_board(chess.Board(), title="chess, start");
"""),
md("""
Layer 1 again. Twenty boards this time, and this is the smallest layer the chess tree will ever have.
"""),
code("""
from seminarlab.lab1.chessgame import Chess
draw_first_moves(Chess());
"""),
code("""
counts_chess = [1]
for depth in range(1, 5):
    start = time.time()
    n = perft(chess.Board(), depth)
    counts_chess.append(n)
    print(f"layer {depth}: {n:>12,} boards   ({time.time() - start:.1f} s)")
"""),
md("""
**Try this.** Add `5` to the range above, so it reads `range(1, 6)`. Layer 5 has 4,865,609 boards and takes between ten seconds and a minute. Layer 6 has 119 million and would take a long lunch. Layer 10 has about 69 trillion. Nobody has counted layer 20.
"""),
code("""
bar_per_layer(counts_chess, "Chess: boards in each layer (first four moves)", log=True);
"""),
md("""
## 4. Against the universe

We cannot count the whole chess tree, so we estimate it the way Claude Shannon did in 1950: about 35 choices per move, about 80 moves per game, so 35^80, which is about 10^120. That is Minsky's number.

Here are the numbers next to each other. The red bar is the number of atoms in the observable universe.
"""),
code("""
from seminarlab.lab1.plots import bar_against_the_universe
bar_against_the_universe();
"""),
md("""
Read the chart from left to right.

- Tic-tac-toe: a quarter of a million games. A laptop does it in a blink.
- Checkers: 10^20 positions. Eighteen years of computing, and done.
- Chess positions: 10^44. Nobody has done it. Nobody will.
- Atoms in the universe: 10^80.
- Chess games: 10^120. If every atom in the universe were a computer, and each one had been checking one game per second since the Big Bang, together they would have checked about 10^97 games. Not close.

So Minsky's sentence is not a figure of speech. There is no hardware, and there never will be, that plays chess by looking at every game. And yet programs play chess, and in 1961 they already did. Minsky's answer is in the sentence right after the one we quoted:

> "Certainly we must use whatever we know in advance to guide the trial generator."

In other words: do not look at everything. Look a few moves ahead, guess how good the position is, and stop. He calls such a guess a **heuristic**. Part B is about that.

## For the room

Dreyfus, in the chapter you read, says the early researchers mistook the first steps for the whole journey. Tic-tac-toe was solved in the 1950s and chess took until 1997, and the method is the same. Was the problem a matter of size, or did something else have to change? Keep the question; Part B gives you more to go on.
"""),
]
