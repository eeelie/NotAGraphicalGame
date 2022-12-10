
from __future__ import annotations
import random
from GraphState import *
from StateClass import State

def start_game() -> State:
    BALL_RAD = 0.05715/2
    standard_ball_positions = [(0, 0.635), (-0.0286, 0.6846), (0.0288, 0.6848), (-0.0572, 0.7342), (0.00020, 0.7344), (0.0576, 0.7346), (-0.0858, 0.7838), (-0.0284, 0.784), (0.0289, 0.7842), (0.0864, 0.7844), (-0.1144, 0.8334), (-0.057, 0.8336), (0.0004, 0.8338), (0.0578, 0.834), (0.1152, 0.8342)]

    eight_pos = standard_ball_positions.pop(4)
    cue_pos = (0, -0.635)

    # randomize ball positions
    random.shuffle(standard_ball_positions)

    # create ball objects
    game_balls = {}
    i = 0
    for coords in standard_ball_positions:
        if i == 0:
            game_balls[i] = Ball(i, BALL_RAD, cue_pos[0], cue_pos[1], 0, 0)
            i += 1
        elif i == 8:
            game_balls[i] = Ball(i, BALL_RAD, eight_pos[0], eight_pos[1], 0, 0)
            i += 1

        game_balls[i] = Ball(i, BALL_RAD, coords[0], coords[1], 0, 0)
        i += 1

    graph_state(game_balls)

    initial_state = State(game_balls)


    return initial_state

