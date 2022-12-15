from game import Game
from visualize import graph_state
import pytest
from pytest import raises

def start_game_graph():
    game = Game("A", "B")
    game.start_game()
    return game

@pytest.mark.mpl_image_compare
def test_initial_graph():
    fig = graph_state(start_game_graph().running_state)
    return fig

@pytest.mark.mpl_image_compare
def test_update_changes_graph():
    game = start_game_graph()
    game.update_state(12, 87)
    return graph_state(game.running_state)