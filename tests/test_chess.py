import chess

from seminarlab.lab1.chessgame import Chess, perft
from seminarlab.lab1.search import minimax


def test_perft_matches_known_values():
    assert perft(chess.Board(), 1) == 20
    assert perft(chess.Board(), 2) == 400
    assert perft(chess.Board(), 3) == 8902


def test_evaluation_is_zero_at_start_and_symmetric():
    g = Chess()
    assert g.evaluate(g.initial()) == 0.0
    b = chess.Board("4k3/8/8/8/8/8/8/4K2R w - - 0 1")
    assert g.evaluate(b) == 5.0


def test_search_finds_mate_in_one():
    g = Chess()
    b = chess.Board("6k1/5ppp/8/8/8/8/8/R5K1 w - - 0 1")
    _, move = minimax(g, b, 2)
    assert move == chess.Move.from_uci("a1a8")
