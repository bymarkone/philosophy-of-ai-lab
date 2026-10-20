from seminarlab.lab1.search import (
    Counter,
    count_layers,
    minimax,
    unique_positions_per_layer,
)
from seminarlab.lab1.tictactoe import MAX, TicTacToe


def test_tree_size_matches_known_figure():
    g = TicTacToe()
    assert sum(count_layers(g, g.initial(), 9)) == 549_946


def test_unique_positions_matches_known_figure():
    g = TicTacToe()
    assert sum(unique_positions_per_layer(g, g.initial(), 9)) == 5_478


def test_perfect_play_is_a_draw():
    g = TicTacToe()
    s = g.initial()
    while not g.is_over(s):
        _, m = minimax(g, s, 9)
        s = g.play(s, m)
    assert g.winner(s) == 0


def test_minimax_takes_the_winning_move():
    g = TicTacToe()
    # X X . / O . . / O . .   X to move, must win at 2
    s = ("X", "X", " ", "O", " ", " ", "O", " ", " ")
    assert g.to_move(s) == MAX
    _, m = minimax(g, s, 9)
    assert m == 2


def test_alpha_beta_visits_fewer_nodes_than_full_tree():
    g = TicTacToe()
    c = Counter()
    minimax(g, g.initial(), 9, c)
    assert c.nodes < 549_946


def test_minimax_prefers_the_quicker_win():
    g = TicTacToe()
    # X . . / . O . / X . O   X to move: square 3 wins now, square 1 wins later
    s = ("X", " ", " ", " ", "O", " ", "X", " ", "O")
    _, m = minimax(g, s, 9)
    assert m == 3
