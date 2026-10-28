import chess
import matplotlib

matplotlib.use("Agg")

from seminarlab.lab1 import boards
from seminarlab.lab1.checkers import Checkers


def test_pieces_of_checkers_start_has_twelve_a_side_on_dark_squares():
    pieces = boards.pieces_of(Checkers().initial())
    assert sum(colour == "white" for _, colour, _ in pieces.values()) == 12
    assert sum(colour == "black" for _, colour, _ in pieces.values()) == 12
    assert all((r + c) % 2 == 1 for r, c in pieces)


def test_pieces_of_chess_puts_white_king_on_e1_bottom_row():
    pieces = boards.pieces_of(chess.Board())
    assert pieces[(7, 4)] == ("glyph", "white", "♚")
    assert pieces[(0, 3)] == ("glyph", "black", "♛")


def test_changed_squares_is_from_and_to_of_the_move():
    b = chess.Board()
    after = b.copy()
    after.push_san("e4")
    assert boards.changed_squares(b, after) == {(6, 4), (4, 4)}


def test_film_shows_start_and_end():
    game = Checkers()
    s0 = game.initial()
    history = [s0, game.play(s0, game.moves(s0)[0])]
    fig = boards.draw_film(history, every=5)
    assert len([ax for ax in fig.axes if ax.has_data()]) == 2


def test_first_moves_draws_one_board_per_move():
    game = Checkers()
    fig = boards.draw_first_moves(game)
    assert len([ax for ax in fig.axes if ax.has_data()]) == 1 + len(game.moves(game.initial()))
