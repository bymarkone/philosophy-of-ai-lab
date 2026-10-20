"""Tic-tac-toe with the common game interface used by the lab's one minimax.

A state is a tuple of 9 characters: 'X', 'O' or ' '. X moves first and is
the maximising player (+1). O is the minimising player (-1).
"""

from __future__ import annotations

LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)

MAX, MIN = 1, -1


class TicTacToe:
    name = "tic-tac-toe"

    def initial(self):
        return (" ",) * 9

    def to_move(self, state):
        return MAX if state.count("X") == state.count("O") else MIN

    def moves(self, state):
        return [i for i, cell in enumerate(state) if cell == " "]

    def play(self, state, move):
        mark = "X" if self.to_move(state) == MAX else "O"
        return state[:move] + (mark,) + state[move + 1:]

    def winner(self, state):
        for a, b, c in LINES:
            if state[a] != " " and state[a] == state[b] == state[c]:
                return MAX if state[a] == "X" else MIN
        return 0

    def is_over(self, state):
        return self.winner(state) != 0 or " " not in state

    def evaluate(self, state):
        return float(self.winner(state))

    def render(self, state):
        return "\n".join(
            " | ".join(c if c != " " else "." for c in state[r * 3:(r + 1) * 3]) for r in range(3)
        )
