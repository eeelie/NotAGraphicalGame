from game import *
from pytest import raises


def test_ball_team():
    assert ball_team(0) == "cue"
    for i in range(1, 8):
        assert ball_team(i) == "solids"
    assert ball_team(8) == "eight"
    for i in range(9, 16):
        assert ball_team(i) == "stripes"


def test_bad_team():
    with raises(Exception):
        ball_team(-1)
        ball_team(16)
        ball_team("one")


def test_ball_team_random():
    for i in range(20):
        ID = random.randint(-30, 30)
        if ID < 0 or ID > 15:
            with raises(Exception):
                ball_team(ID)
        elif ID == 0:
            assert ball_team(0) == "cue"
        elif ID == 8:
            assert ball_team(8) == "eight"
        elif 1 <= ID <= 7:
            assert ball_team(ID) == "solids"
        elif 9 <= ID <= 15:
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
        player = random.randint(-5, 5)
        if player == 1:
            assert other_player(player) == 0
        elif player == 0:
            assert other_player(0) == 1
        else:
            with raises(Exception):
                other_player(player)


def test_take_input_force(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 3)
    force = float(input("Input a velocity in m/s"))
    assert force == 3


def test_constructor():
    game1 = Game("Hayden", "Jose")

    assert game1.players == [Player("Hayden"), Player("Jose")]

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
    ball_dict = {
        0: Ball(0, 0.028575, 0, -0.635, 0, 0),
        1: Ball(1, 0.028575, 0.1152, 0.8342, 0, 0),
        2: Ball(2, 0.028575, -0.057, 0.8336, 0, 0),
        3: Ball(3, 0.028575, 0, 0.635, 0, 0),
        4: Ball(4, 0.028575, 0.0578, 0.834, 0, 0),
        5: Ball(5, 0.028575, -0.0284, 0.784, 0, 0),
        6: Ball(6, 0.028575, -0.0858, 0.7838, 0, 0),
        7: Ball(7, 0.028575, -0.0572, 0.7342, 0, 0),
        8: Ball(8, 0.028575, 0.0002, 0.7344, 0, 0),
        9: Ball(9, 0.028575, 0.0864, 0.7844, 0, 0),
        10: Ball(10, 0.028575, 0.0289, 0.7842, 0, 0),
        11: Ball(11, 0.028575, 0.0004, 0.8338, 0, 0),
        12: Ball(12, 0.028575, 0.0576, 0.7346, 0, 0),
        13: Ball(13, 0.028575, -0.0286, 0.6846, 0, 0),
        14: Ball(14, 0.028575, -0.1144, 0.8334, 0, 0),
        15: Ball(15, 0.028575, 0.0288, 0.6848, 0, 0),
    }
    game1 = Game("Hayden", "Jose")
    game1.start_game(1)

    assert game1.running_state == State(ball_dict)


def test_current_player_name():
    game1 = Game("Jack", "Elie")
    game1.start_game()
    ID = game1.current_player_id
    if ID == 0:
        assert game1.current_player_name() == game1.players[0].name
    elif game1.current_player_id == 1:
        assert game1.current_player_name() == game1.players[1].name


def test_update_state():
    game1 = Game("Elie", "Jose")
    game1.start_game(1)

    ball_dict = {
        0: Ball(0, 0.028575, 0, -0.635, 0, 0),
        1: Ball(1, 0.028575, 0.1152, 0.8342, 0, 0),
        2: Ball(2, 0.028575, -0.057, 0.8336, 0, 0),
        3: Ball(3, 0.028575, 0, 0.635, 0, 0),
        4: Ball(4, 0.028575, 0.0578, 0.834, 0, 0),
        5: Ball(5, 0.028575, -0.0284, 0.784, 0, 0),
        6: Ball(6, 0.028575, -0.0858, 0.7838, 0, 0),
        7: Ball(7, 0.028575, -0.0572, 0.7342, 0, 0),
        8: Ball(8, 0.028575, 0.0002, 0.7344, 0, 0),
        9: Ball(9, 0.028575, 0.0864, 0.7844, 0, 0),
        10: Ball(10, 0.028575, 0.0289, 0.7842, 0, 0),
        11: Ball(11, 0.028575, 0.0004, 0.8338, 0, 0),
        12: Ball(12, 0.028575, 0.0576, 0.7346, 0, 0),
        13: Ball(13, 0.028575, -0.0286, 0.6846, 0, 0),
        14: Ball(14, 0.028575, -0.1144, 0.8334, 0, 0),
        15: Ball(15, 0.028575, 0.0288, 0.6848, 0, 0),
    }
    state1 = State(ball_dict)

    for i in range(20):
        velocity = round(random.uniform(0.0, 5.0), 2)
        angle = round(random.uniform(-360.0, 360.0), 2)
        game1.update_state(velocity, angle)
        state1.update(velocity, angle)
        assert game1.running_state == state1


def test_pocketed_this_turn():
    ...


def test_update_players():
    ...


def test_winner():
    ...


def test_next_player():
    ...
