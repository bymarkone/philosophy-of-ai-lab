from tools.nb import code, md, setup


def cells():
    return [
md("""
# Part B — One search, three games

In Part A we saw that nobody can look at every game of chess. This part is about what a program does instead. The method was written down by Shannon in 1950 and used in every game-playing program since. It is called **minimax**, and the version with a shortcut is called **alpha-beta**. Here it is, in full. Thirty lines. Read it once; the explanation follows.
"""),
setup(),
code("""
import math

MAX, MIN = 1, -1      # the two players. MAX wants a high score, MIN a low one.

class Counter:
    def __init__(self):
        self.nodes = 0

def minimax(game, board, depth, counter, alpha=-math.inf, beta=math.inf):
    counter.nodes += 1
    if game.is_over(board):                          # game finished: a win found sooner counts more
        return game.evaluate(board) * (1 + depth), None
    if depth == 0:                                   # stop looking: how good is this board?
        return game.evaluate(board), None

    best_move = None
    if game.to_move(board) == MAX:                   # my turn: pick the move with the highest value
        best = -math.inf
        for move in game.moves(board):
            value, _ = minimax(game, game.play(board, move), depth - 1, counter, alpha, beta)
            if value > best:
                best, best_move = value, move
            alpha = max(alpha, best)
            if alpha >= beta:                        # the opponent will never let us get here
                break
    else:                                            # their turn: they pick the lowest value
        best = math.inf
        for move in game.moves(board):
            value, _ = minimax(game, game.play(board, move), depth - 1, counter, alpha, beta)
            if value < best:
                best, best_move = value, move
            beta = min(beta, best)
            if alpha >= beta:
                break
    return best, best_move


def play_game(game, depth_for, counter, max_plies=200):
    # Let minimax play both sides. depth_for says how far ahead each player looks.
    board = game.initial()
    history = [board]
    for _ in range(max_plies):
        if game.is_over(board):
            break
        _, move = minimax(game, board, depth_for[game.to_move(board)], counter)
        board = game.play(board, move)
        history.append(board)
    return history
"""),
md("""
## What it does

The idea fits in one sentence: **look a few moves ahead, assume the other side plays the best reply it can, and pick the move that leaves you best off.**

- `depth` is how many moves ahead to look. When it reaches zero, the function stops and asks the game for a guess: `game.evaluate(board)`. That guess is the heuristic. In tic-tac-toe it is +1 for an X win, −1 for an O win, 0 otherwise. In chess it counts the pieces.
- `MAX` wants a high score and picks the maximum. `MIN` wants a low score and picks the minimum. Hence the name.
- `alpha` and `beta` remember the best each side can already guarantee. When a branch cannot change the answer, the loop stops early. That is the whole of alpha-beta. It does not change the result, only the number of boards looked at.

Below it is a ten-line loop that lets the function play both sides of a game. That is all the machinery there is.

Notice what is not in the search function: nothing about chess, nothing about checkers, nothing about X and O. The function only asks the game four questions: whose turn, what moves, what happens after a move, how good is it. Any game that can answer those four questions can be played by this function.

## 1. Tic-tac-toe

Nine moves ahead is the whole game, so the function plays perfectly.
"""),
code("""
from seminarlab.lab1.tictactoe import TicTacToe
import time

ttt = TicTacToe()
counter = Counter()
start = time.time()
history = play_game(ttt, depth_for={MAX: 9, MIN: 9}, counter=counter)
print(ttt.render(history[-1]))
print()
print("result:", {1: "X wins", -1: "O wins", 0: "draw"}[ttt.winner(history[-1])])
print(f"boards looked at: {counter.nodes:,}   time: {time.time() - start:.2f} s")
"""),
md("""
A draw, as it should be. And it looked at about 18,000 boards, not the 549,946 in the tree, because of alpha-beta.

**Try this.** Play against it. You are X. Put your moves in the list below (cells are numbered 0 to 8, left to right, top to bottom). The computer answers each one. Try to win.
"""),
code("""
my_moves = [4, 1, 3, 2, 8]          # change these

board = ttt.initial()
for my_move in my_moves:
    if ttt.is_over(board) or my_move not in ttt.moves(board):
        break
    board = ttt.play(board, my_move)                      # your move
    if not ttt.is_over(board):
        _, reply = minimax(ttt, board, 9, Counter())      # its move
        board = ttt.play(board, reply)
print(ttt.render(board))
print()
print({1: "you won", -1: "it won", 0: "draw"}.get(ttt.winner(board)) if ttt.is_over(board) else "game not over yet, add moves")
"""),
md("""
## 2. Checkers

Same function. Different game. The game can no longer be read to the end, so we give it a depth and an evaluation: count the pieces, a king is worth one and a half men.

Let's have white look 3 moves ahead and black 2, and see who wins.
"""),
code("""
from seminarlab.lab1.checkers import Checkers

checkers = Checkers()
counter = Counter()
start = time.time()
history = play_game(checkers, depth_for={MAX: 3, MIN: 2}, max_plies=150, counter=counter)
final = history[-1]
print("pieces left:", checkers.count_pieces(final))
print("moves played:", len(history) - 1, "  boards looked at:", f"{counter.nodes:,}", f"  time: {time.time() - start:.1f} s")
"""),
md("""
Here is the game, one board every six moves. The last move is marked on each board. A star is a king.
"""),
code("""
from seminarlab.lab1.boards import draw_film
from seminarlab.lab1.plots import plot_opinion, bar_pruning

draw_film(history, every=6);
"""),
md("""
And here is what the program thought after every move. This is the only thing it ever "sees" of the game: one number, white's pieces minus black's. Each step in the line is a capture.
"""),
code("""
plot_opinion([checkers.evaluate(board) for board in history]);
"""),
md("""
White, who sees one move further, wins with pieces to spare. The line stays near zero for thirty moves, then climbs. That is the whole business model of computer chess: see further than the other side.

**Try this.** Swap them: `{MAX: 2, MIN: 3}`. Then make it even. Then try `{MAX: 8, MIN: 4}`, which takes a minute, and watch white win again.

**And try this,** because it is not as simple as "deeper always wins": `{MAX: 4, MIN: 2}`. White, seeing twice as far, drifts into a draw and ends up behind on material. The guess at the end of the look-ahead is still a guess, and a guess made four moves out can be worse than one made two moves out, if a capture is waiting just beyond the horizon. Engine builders call this the horizon effect, and much of what makes a real engine strong is handling it. Also, two programs with fixed rules play the same game every time, so one unlucky line is unlucky forever.
"""),
md("""
## 3. Chess

Same function a third time. The evaluation counts material: pawn 1, knight 3, bishop 3, rook 5, queen 9. First, let's see how the number of boards grows with depth. This is Part A's tree again, but now with alpha-beta cutting branches.
"""),
code("""
from seminarlab.lab1.chessgame import Chess

chess_game = Chess()
searched = []
for depth in range(1, 6):
    counter = Counter()
    start = time.time()
    value, move = minimax(chess_game, chess_game.initial(), depth, counter)
    searched.append(counter.nodes)
    print(f"depth {depth}: {counter.nodes:>9,} boards   {time.time() - start:6.1f} s   plays {move}")
"""),
md("""
Put that next to the full tree from Part A. Grey is every board in the tree at that depth; blue is what alpha-beta actually looked at to find the same answer. The gap is the shortcut, and it grows with depth.
"""),
code("""
in_the_tree = [20, 400, 8_902, 197_281, 4_865_609]      # counted in Part A
bar_pruning(in_the_tree, searched);
"""),
md("""
**Try this.** Change `range(1, 6)` to `range(1, 7)`. Depth 6 takes around a minute. Depth 7 is a coffee break. Depth 10 is overnight. The strongest engines today look 20 or more moves ahead, and they do it with better shortcuts, not more patience.

**Try this, too.** Go back to the `minimax` cell at the top, delete the two lines that say `if alpha >= beta: break`, run that cell, and run the table again. Without the shortcut, depth 4 looks at about 200,000 boards instead of 6,000. Same answer. Then put the lines back.
"""),
md("""
Now let it play a few moves against itself, three moves deep.
"""),
code("""
counter = Counter()
start = time.time()
history = play_game(chess_game, depth_for={MAX: 3, MIN: 3}, max_plies=12, counter=counter)
print(f"12 moves, {counter.nodes:,} boards, {time.time() - start:.1f} s")
draw_film(history, every=2);
"""),
md("""
Not good chess. Three moves ahead and a count of the pieces gets you a program that does not hang its queen and not much more. But it is chess, and it is the same thirty lines that drew tic-tac-toe.

## 4. Change what "good" means

The evaluation is the only place the program has any opinion. Here it is for chess:
"""),
code("""
import inspect
print(inspect.getsource(chess_game.evaluate))
"""),
md("""
**Try this.** Build a chess game where a knight is worth 9 and a queen 1, then let it play 12 moves. Watch what it does with its knights. Then set every piece to 0 and see what it does with nothing to care about.
"""),
code("""
import chess

odd_values = {chess.PAWN: 1, chess.KNIGHT: 9, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 1, chess.KING: 0}
odd_chess = Chess(piece_value=odd_values)         # change the numbers above

history = play_game(odd_chess, depth_for={MAX: 3, MIN: 3}, max_plies=12, counter=Counter())
draw_film(history, every=2);
"""),
md("""
## What just happened

Turing imagined this in 1950, as one of the sample questions in his test:

> Q: Do you play chess?
> A: Yes.
> Q: I have K at my K1, and no other pieces. You have only K at K6 and R at R1. It is your move. What do you play?
> A: (After a pause of 15 seconds) R-R8 mate.
>
> — Turing, *Computing Machinery and Intelligence*, section 1

The function above answers that question correctly, and it answers it the way Turing describes: a pause, then the move. What Turing does not say is what happens during the pause, and now you know. It is the loop you just read.

Searle, thirty years later, says this about exactly this kind of program:

> "The computer, to repeat, has a syntax but no semantics. Thus, if you type into the computer '2 plus 2 equals?' it will type out '4.' But it has no idea that '4' means 4 or that it means anything at all."
>
> — Searle, *Minds, Brains, and Programs*

Look back at the thirty lines. There is no chess in them. The word "move" is a name we chose; the function would work the same if we called it "thing". It does not know that the board is a board, that X is a mark, that a queen is worth having. It compares numbers. When it beat you at tic-tac-toe, it did not know it was playing.

## For the room

Two questions, pick one.

1. Searle says the program manipulates symbols without understanding them. Fine. But where is the understanding when *you* play tic-tac-toe? You also look ahead and pick the best. Is the difference what you do, or something about you?
2. Turing ends his paper by wondering whether to start with "a very abstract activity, like the playing of chess" or to "provide the machine with the best sense organs that money can buy, and then teach it to understand and speak English". Chess fell first. Why was that the easy one?
"""),
]
