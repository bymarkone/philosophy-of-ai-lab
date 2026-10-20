"""Chess with the common game interface. Rules come from python-chess.

The search, the evaluation and the counting are ours. python-chess only
tells us which moves are legal and whether the game is over.
"""

from __future__ import annotations

import chess

MAX, MIN = 1, -1

PIECE_VALUE = {
    chess.PAWN: 1.0,
    chess.KNIGHT: 3.0,
    chess.BISHOP: 3.0,
    chess.ROOK: 5.0,
    chess.QUEEN: 9.0,
    chess.KING: 0.0,
}

CENTRE = {chess.D4, chess.E4, chess.D5, chess.E5}


class Chess:
    name = "chess"

    def __init__(self, piece_value=None):
        """piece_value: what each piece is worth to the evaluation. Pass a
        dict to play with different values; the default table is not changed."""
        self.piece_value = dict(piece_value or PIECE_VALUE)

    def initial(self):
        return chess.Board()

    def to_move(self, state):
        return MAX if state.turn == chess.WHITE else MIN

    def moves(self, state):
        return list(state.legal_moves)

    def play(self, state, move):
        new = state.copy(stack=False)
        new.push(move)
        return new

    def is_over(self, state):
        return state.is_game_over()

    def winner(self, state):
        if state.is_checkmate():
            return MIN if state.turn == chess.WHITE else MAX
        return 0

    def evaluate(self, state):
        """Material from white's point of view, plus a small bonus for
        pawns and knights in the centre. Checkmate is worth 100."""
        if state.is_checkmate():
            return 100.0 * self.winner(state)
        if state.is_game_over():
            return 0.0
        score = 0.0
        for square, piece in state.piece_map().items():
            value = self.piece_value[piece.piece_type]
            if square in CENTRE and piece.piece_type in (chess.PAWN, chess.KNIGHT):
                value += 0.2
            score += value if piece.color == chess.WHITE else -value
        return score

    def render(self, state):
        return str(state) + ("\nwhite to move" if state.turn else "\nblack to move")


def perft(board, depth):
    """Number of leaf positions after `depth` plies. Standard chess count."""
    if depth == 0:
        return 1
    total = 0
    for move in board.legal_moves:
        board.push(move)
        total += perft(board, depth - 1)
        board.pop()
    return total
