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

    assert player1.balls_left == [9, 10, 11, 12, 13, 14, 15]
    assert player2.balls_left == [1, 2, 3, 4, 5, 6, 7]


def test_assign_bad_team_name():
    with raises(Exception):
        bad_player = "Hayden"
        bad_player.assign_team("polka-dots")


def test_update_balls_left():
    pocketed = [1, 5, 12]
    player1 = Player("Jose")
    player2 = Player("Elie")
    player3 = Player("Jack")
    player1.assign_team("solids")
    player2.assign_team("stripes")

    assert player1.balls_left == [1, 2, 3, 4, 5, 6, 7]
    assert player2.balls_left == [9, 10, 11, 12, 13, 14, 15]
    assert player3.balls_left == []

    player1.update_balls_left(pocketed)
    player2.update_balls_left(pocketed)
    player3.update_balls_left(pocketed)

    assert player1.balls_left == [2, 3, 4, 6, 7]
    assert player2.balls_left == [9, 10, 11, 13, 14, 15]
    assert player3.balls_left == []

    assert player1.down_to_the_eight == False
    assert player2.down_to_the_eight == False
