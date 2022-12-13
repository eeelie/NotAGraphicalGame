from player import *
from pytest import raises

def test_constructor():
    player1 = Player("Hayden")
    player2 = Player("Jose")

    assert player1.name == "Hayden"
    assert player1.team == "undefined"
    assert player1.balls_left == []
    assert player1.down_to_the_eight == False
    assert player2.name == "Jose"
    assert player1.team == "undefined"
    assert player1.balls_left == []
    assert player1.down_to_the_eight == False
    
def test_assign_team():
    player1 = Player("Elie")
    player2 = Player("Jack")
    player1.assign_team("stripes")
    player2.assign_team("solids")

    assert player1.team == "stripes"
    assert player2.team == "solids"

def test_assign_bad_team_name():
    with raises(Exception):
        bad_player = ("Hayden")
        bad_player.assign_team("polka-dots")

def test_update_balls_left():
    ...    
