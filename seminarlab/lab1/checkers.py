"""English checkers (draughts) on an 8x8 board, with forced captures.

Board rows go from 0 (top) to 7 (bottom). Pieces sit on dark squares only,
where (row + col) is odd. 'w'/'W' are white men/kings, 'b'/'B' black.
White starts at the bottom and moves up (towards row 0). Black starts at
the top and moves down. White moves first and is the maximising player.

A move is a tuple of squares: (from, to) for a step, and for a capture
(from, landing1, landing2, ...), one landing square per jump.
"""

from __future__ import annotations

MAX, MIN = 1, -1
SIZE = 8


def _start_board():
    rows = []
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            dark = (r + c) % 2 == 1
            if dark and r < 3:
                row.append("b")
            elif dark and r > 4:
                row.append("w")
            else:
                row.append(".")
        rows.append(tuple(row))
    return tuple(rows)


def _inside(r, c):
    return 0 <= r < SIZE and 0 <= c < SIZE


def _owner(piece):
    if piece in "wW":
        return MAX
    if piece in "bB":
        return MIN
    return 0


def _directions(piece):
    if piece == "w":
        return ((-1, -1), (-1, 1))
    if piece == "b":
        return ((1, -1), (1, 1))
    return ((-1, -1), (-1, 1), (1, -1), (1, 1))


def _set(board, r, c, piece):
    row = board[r][:c] + (piece,) + board[r][c + 1:]
    return board[:r] + (row,) + board[r + 1:]


def _captures_from(board, r, c, piece, path):
    """All maximal jump sequences starting at (r, c)."""
    results = []
    for dr, dc in _directions(piece):
        mr, mc = r + dr, c + dc
        lr, lc = r + 2 * dr, c + 2 * dc
        if not _inside(lr, lc):
            continue
        if _owner(board[mr][mc]) == -_owner(piece) and board[lr][lc] == ".":
            nb = _set(_set(_set(board, r, c, "."), mr, mc, "."), lr, lc, piece)
            further = _captures_from(nb, lr, lc, piece, path + ((lr, lc),))
            results.extend(further if further else [path + ((lr, lc),)])
    return results


class Checkers:
    name = "checkers"

    def initial(self):
        return (_start_board(), MAX)

    def to_move(self, state):
        return state[1]

    def moves(self, state):
        board, player = state
        captures, steps = [], []
        for r in range(SIZE):
            for c in range(SIZE):
                piece = board[r][c]
                if _owner(piece) != player:
                    continue
                captures.extend(_captures_from(board, r, c, piece, ((r, c),)))
                for dr, dc in _directions(piece):
                    nr, nc = r + dr, c + dc
                    if _inside(nr, nc) and board[nr][nc] == ".":
                        steps.append(((r, c), (nr, nc)))
        return captures if captures else steps

    def play(self, state, move):
        board, player = state
        (r, c), rest = move[0], move[1:]
        piece = board[r][c]
        board = _set(board, r, c, ".")
        for nr, nc in rest:
            if abs(nr - r) == 2:
                board = _set(board, (r + nr) // 2, (c + nc) // 2, ".")
            r, c = nr, nc
        if piece == "w" and r == 0:
            piece = "W"
        if piece == "b" and r == SIZE - 1:
            piece = "B"
        board = _set(board, r, c, piece)
        return (board, -player)

    def is_over(self, state):
        return not self.moves(state)

    def winner(self, state):
        return -state[1] if self.is_over(state) else 0

    def evaluate(self, state):
        """Material from white's point of view: a man is 1, a king is 1.5.
        A small bonus for men that have advanced, so play is not passive."""
        if self.is_over(state):
            return 100.0 * self.winner(state)
        board, _ = state
        score = 0.0
        for r in range(SIZE):
            for c in range(SIZE):
                p = board[r][c]
                if p == "w":
                    score += 1 + 0.02 * (SIZE - 1 - r)
                elif p == "W":
                    score += 1.5
                elif p == "b":
                    score -= 1 + 0.02 * r
                elif p == "B":
                    score -= 1.5
        return score

    def render(self, state):
        board, player = state
        lines = ["  " + " ".join(str(c) for c in range(SIZE))]
        for r in range(SIZE):
            lines.append(f"{r} " + " ".join(board[r]))
        lines.append(f"{'white' if player == MAX else 'black'} to move")
        return "\n".join(lines)

    def count_pieces(self, state):
        board, _ = state
        flat = [p for row in board for p in row]
        return {p: flat.count(p) for p in "wWbB"}
