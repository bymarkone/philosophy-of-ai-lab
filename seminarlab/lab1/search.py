"""Minimax with alpha-beta pruning, and tree counting.

The notebook for Part B shows this same function in full. It lives here
too so that tests and the other notebooks can use it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

MAX, MIN = 1, -1


@dataclass
class Counter:
    nodes: int = 0


def minimax(game, state, depth, counter=None, alpha=-math.inf, beta=math.inf):
    """Return (value, best_move) for `state`, looking `depth` moves ahead.

    Value is from the maximising player's point of view. The maximiser
    picks the child with the highest value, the minimiser the lowest.
    Alpha and beta remember the best each side can already guarantee, so
    branches that cannot change the answer are skipped.
    """
    if counter is not None:
        counter.nodes += 1
    if game.is_over(state):
        return game.evaluate(state) * (1 + depth), None   # a win found sooner counts more
    if depth == 0:
        return game.evaluate(state), None

    best_move = None
    if game.to_move(state) == MAX:
        best = -math.inf
        for move in game.moves(state):
            value, _ = minimax(game, game.play(state, move), depth - 1, counter, alpha, beta)
            if value > best:
                best, best_move = value, move
            alpha = max(alpha, best)
            if alpha >= beta:
                break
    else:
        best = math.inf
        for move in game.moves(state):
            value, _ = minimax(game, game.play(state, move), depth - 1, counter, alpha, beta)
            if value < best:
                best, best_move = value, move
            beta = min(beta, best)
            if alpha >= beta:
                break
    return best, best_move


def count_layers(game, state, max_depth):
    """Number of nodes in each layer of the full game tree, root included.

    The tree stops at finished games. Returns a list: layer 0 has one node,
    layer 1 has as many nodes as there are first moves, and so on.
    """
    counts = [0] * (max_depth + 1)

    def walk(s, depth):
        counts[depth] += 1
        if depth == max_depth or game.is_over(s):
            return
        for move in game.moves(s):
            walk(game.play(s, move), depth + 1)

    walk(state, 0)
    return counts


def unique_positions_per_layer(game, state, max_depth):
    """Like count_layers, but a position reached by different move orders
    is counted once per layer. Needs states that can go in a set, which
    tic-tac-toe and checkers states can and chess boards cannot."""
    layer = {state}
    counts = [1]
    for _ in range(max_depth):
        nxt = set()
        for s in layer:
            if game.is_over(s):
                continue
            for move in game.moves(s):
                nxt.add(game.play(s, move))
        if not nxt:
            break
        counts.append(len(nxt))
        layer = nxt
    return counts


def play_game(game, depth_for, max_plies=200, counter=None):
    """Let minimax play both sides. `depth_for` maps player (+1/-1) to depth.
    Returns the list of states visited, last one included."""
    state = game.initial()
    history = [state]
    for _ in range(max_plies):
        if game.is_over(state):
            break
        _, move = minimax(game, state, depth_for[game.to_move(state)], counter)
        if move is None:
            break
        state = game.play(state, move)
        history.append(state)
    return history
