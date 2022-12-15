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
    game1 = Game("Elie","Jose")
    game1.start_game(1)
    
    assert game1.pocketed_this_turn() == []
    game1.update_state(3,45)
    assert game1.pocketed_this_turn() == [0]
    
    for i in range(10):
        game1.start_game(1)
        rand_ball = random.randint(0,15)
        game1.running_state.pocketed = [rand_ball]
        assert game1.pocketed_this_turn() == [rand_ball]

    game2 = Game("Hayden","Jack")
    game2.start_game(1)
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
        game2.update_state(velocity, angle)
        state1.update(velocity, angle)
        assert game2.pocketed_this_turn() == state1.pocketed

    
def test_update_players():
    game1 = Game("Elie","Jose")
    game1.start_game(1)

    game1.running_state.pocketed = [2,7,10]

    assert game1.players[0].balls_left == [1,2,3,4,5,6,7]
    assert game1.players[1].balls_left == [9,10,11,12,13,14,15]

    game1.update_players()
    assert game1.players[0].balls_left == [1,3,4,5,6]
    assert game1.players[1].balls_left == [9,11,12,13,14,15]
    


def test_winner():
    # Player 0 sinks 8 ball, but still has balls left; Player 1 not down to 8 -> Player 1 wins
    game1 = Game("Jack","Jose")
    game1.start_game(1)
    game1.current_player_id = 0
    game1.running_state.pocketed = [8]
    assert game1.players[1].down_to_the_eight  == False
    assert game1.winner() == "Jose"

    # Player 0 sinks 8 ball, but still has balls left; Player 1 down to 8 -> Player 1 wins
    game2 = Game("Jack","Jose")
    game2.start_game(1)
    game2.current_player_id = 0
    game2.running_state.pocketed = [8]
    game2.players[1].down_to_the_eight == True
    assert game2.winner() == "Jose"

    # Player 1 sinks 8 ball, but still has balls left -> Player 0 wins
    game3 = Game("Jack","Jose")
    game3.start_game(1)
    game3.current_player_id = 1
    game3.running_state.pocketed = [8]
    assert game3.winner() == "Jack"

    # Player 0 down to 8, sinks 8 ball -> Player 0 wins
    game4 = Game("Jack","Jose")
    game4.start_game(1)
    game4.current_player_id = 0
    game4.players[0].down_to_the_eight = True
    game4.running_state.pocketed = [8]
    assert game4.winner() == "Jack"

    # Player 1 down to 8, sinks 8 ball -> Player 1 wins
    game5 = Game("Jack","Jose")
    game5.start_game(1)
    game5.current_player_id = 1
    game5.players[1].down_to_the_eight = True
    game5.running_state.pocketed = [8]
    assert game5.winner() == "Jose"

    # Player 0 down to 8, sinks 8 ball and cue -> Player 1 wins
    game6 = Game("Jack","Jose")
    game6.start_game(1)
    game6.current_player_id = 0
    game6.players[0].down_to_the_eight = True
    game6.running_state.pocketed = [0,8]
    assert game6.winner() == "Jose"

    game7 = Game("Jack","Jose")
    game7.start_game(1)
    game7.current_player_id = 0
    game7.players[0].down_to_the_eight = True
    game7.running_state.pocketed = [8,0]
    assert game7.winner() == "Jose"

    # Player 1 down to 8, sinks 8 ball and cue -> Player 0 wins
    game8 = Game("Jack","Jose")
    game8.start_game(1)
    game8.current_player_id = 1
    game8.players[1].down_to_the_eight = True
    game8.running_state.pocketed = [0,8]
    assert game8.winner() == "Jack"

def test_next_player():

    # No balls pocketed -> current player switches
    game1 = Game("Hayden","Jose")
    game1.start_game(1)
    assert game1.current_player_id == 1
    assert game1.next_player([]) == 0

    game2 = Game("Hayden", "Jose")
    game2.start_game(1)
    game2.current_player_id = 0
    assert game2.current_player_id == 0
    assert game2.next_player([]) == 1

    # Cue ball pocketed -> current player switches
    game3 = Game("Hayden","Jose")
    game3.start_game(1)
    assert game3.current_player_id == 1
    assert game3.next_player([0]) == 0

    game4 = Game("Hayden", "Jose")
    game4.start_game(1)
    game4.current_player_id = 0
    assert game4.current_player_id == 0
    assert game4.next_player([0]) == 1

    # Wrong ball pocketed -> current player switches
    game5 = Game("Hayden","Jose")
    game5.start_game(1)
    assert game5.current_player_id == 1
    assert game5.players[game5.current_player_id].team == "stripes"
    assert game5.next_player([2]) == 0

    game6 = Game("Hayden","Jose")
    game6.start_game(1)
    game6.current_player_id = 0
    assert game6.current_player_id == 0
    assert game6.players[game6.current_player_id].team == "solids"
    assert game6.next_player([11]) == 1

    # Correct ball pocketed -> current player plays again
    game7 = Game("Hayden","Jose")
    game7.start_game(1)
    assert game7.current_player_id == 1
    assert game7.players[game7.current_player_id].team == "stripes"
    assert game7.next_player([2]) == 0

    game8 = Game("Hayden","Jose")
    game8.start_game(1)
    game8.current_player_id = 0
    assert game8.current_player_id == 0
    assert game8.players[game8.current_player_id].team == "solids"
    assert game8.next_player([11]) == 1

    # 8 ball pocketed -> Exception raised
    game9 = Game("Hayden","Jose")
    game9.start_game(1)
    with raises(Exception):
        game9.next_player([8]) == 0
    
