from game import *
from pytest import raises


def test_ball_team():
    assert ball_team(0) == "cue"
    for i in range(1,8):
        assert ball_team(i) == "solids"
    assert ball_team(8) == "eight"
    for i in range(9,16):
        assert ball_team(i) == "stripes"

def test_bad_team():
    with raises(Exception):
        ball_team(-1)
        ball_team(16)
        ball_team("one")

def test_ball_team_random():
    for i in range(20):
        ID = random.randint(-30,30)
        if ID < 0 or ID > 15:
            with raises(Exception):
                ball_team(ID)
        elif ID == 0:
            assert ball_team(0) == "cue"
        elif ID == 8:
            assert ball_team(8) == "eight"
        elif 1 <= ID <=7:
            assert ball_team(ID) == "solids"
        elif 9 <= ID <=15:
            assert ball_team(ID) == "stripes"

def test_other_player():
    assert other_player(1) == 0
    assert other_player(0) == 1

def test_bad_other_player():
    with raises(Exception):
        other_player(3)
        other_player("one")
        other_player()

def test_other_player_random():
    for i in range(20):
        player = random.randint(-5,5)
        if player == 1:
            assert other_player(player) == 0
        elif player == 0:
            assert other_player(0) == 1
        else:
            with raises(Exception):
                other_player(player)

def test_take_input_force(monkeypatch):
    monkeypatch.setattr('builtins.input',lambda _: 3)
    force = float(input("Input a velocity in m/s"))
    assert force == 3

def test_constructor():
    game1 = Game("Hayden","Jose")
    
    assert game1.players == [Player("Hayden"),Player("Jose")]

    assert game1.players[0].name == "Hayden"
    assert game1.players[0].team == "undefined"
    assert game1.players[0].balls_left == []
    assert game1.players[0].down_to_the_eight == False
    assert game1.players[1].name == "Jose"
    assert game1.players[1].team == "undefined"
    assert game1.players[1].balls_left == []
    assert game1.players[1].down_to_the_eight == False

    assert game1.current_player_id == 1 or game1.current_player_id == 0

def test_start_game():
    ...

def test_current_player_name():
    game1 = Game("Jack","Elie")
    game1.start_game()
    ID = game1.current_player_id
    if ID == 0:
        assert game1.current_player_name() == game1.players[0].name
    elif game1.current_player_id == 1:
        assert game1.current_player_name() == game1.players[1].name

def test_update_state():
    ...

def test_pocketed_this_turn():
    ...

def test_update_players():
    ...

def test_winner():
    ...

def test_next_player():
    ...


    