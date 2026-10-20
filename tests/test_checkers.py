import pytest

from seminarlab.lab1.checkers import Checkers
from seminarlab.lab1.search import count_layers, minimax


@pytest.mark.parametrize("depth,expected", [(1, 7), (2, 49), (3, 302), (4, 1469), (5, 7361), (6, 36768)])
def test_perft_matches_known_sequence(depth, expected):
    g = Checkers()
    assert count_layers(g, g.initial(), depth)[depth] == expected


def test_capture_is_forced_and_can_jump_twice():
    board = tuple(tuple("." for _ in range(8)) for _ in range(8))
    board = _put(board, (5, 2), "w")
    board = _put(board, (4, 3), "b")
    board = _put(board, (2, 5), "b")
    g = Checkers()
    moves = g.moves((board, 1))
    assert moves == [((5, 2), (3, 4), (1, 6))]


def test_man_becomes_king_on_last_row():
    board = tuple(tuple("." for _ in range(8)) for _ in range(8))
    board = _put(board, (1, 2), "w")
    board = _put(board, (6, 1), "b")
    g = Checkers()
    nb, _ = g.play((board, 1), ((1, 2), (0, 3)))
    assert nb[0][3] == "W"


def test_search_prefers_winning_material():
    g = Checkers()
    board = tuple(tuple("." for _ in range(8)) for _ in range(8))
    board = _put(board, (5, 2), "w")
    board = _put(board, (4, 3), "b")
    board = _put(board, (0, 7), "b")
    value, move = minimax(g, (board, 1), 2)
    assert move[0] == (5, 2) and len(move) == 2 and value > 0


def _put(board, rc, piece):
    r, c = rc
    row = board[r][:c] + (piece,) + board[r][c + 1:]
    return board[:r] + (row,) + board[r + 1:]
