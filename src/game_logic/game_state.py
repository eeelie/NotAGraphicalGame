from __future__ import annotations
import dataclasses
from src.ball.ball import Ball
import numpy as np
import copy

@dataclasses.dataclass
class GameState:
    balls: dict  # dictionary of all balls in play, keyed by ID
    log: list[dict]  # list of all state dicts
    pocketed: list  # list of ball IDs pocketed since the last turn, in order
    W_TABLE: float
    H_TABLE: float
    BALL_RADIUS: float
    DT: float
    ACCELERATION: float
    WALL_DAMPENING: float

    def __init__(self, initial_balls: dict[int:Ball]):
        "constructor takes dict of Ball objects with ball IDs as the keys"
        self.balls = initial_balls

        self.log = []
        self.pocketed = []
        self.W_TABLE = 1.27  # meters
        self.H_TABLE = 2.54  # meters
        self.BALL_RADIUS = 0.05715 / 2  # meters
        self.DT = 0.01  # seconds
        self.ACCELERATION = 0.1  # m/s^2
        self.WALL_DAMPENING = 0.7

    def modify_simulation_constants(self, dt: float, acc: float, damp: float):
        "modify the time step, acceleration, and wall dampening"
        self.DT = dt
        self.ACCELERATION = acc
        self.WALL_DAMPENING = damp

    def update(self, velocity: float, degrees: float):
        "new update function to run a loop of single updates with helper function update_one_step()"

        balls = copy.deepcopy(self.balls)
        log = []
        pocketed = []

        # provide input to cue ball
        if 0 not in balls:
            balls[0] = Ball(0, self.BALL_RADIUS, 0, -0.635, 0, 0)
        balls[0].v = [velocity, np.radians(degrees)]

        counter = 0

        while True:

            # steps everything forward one step, modifies velocities, returns updated ball dict
            balls = update_one_step(
                balls,
                self.DT,
                self.ACCELERATION,
                self.W_TABLE,
                self.H_TABLE,
                self.WALL_DAMPENING,
            )

            # remove from balls if in pocket
            in_pocket = []
            for ID in balls.keys():
                if balls[ID].in_pocket(self.W_TABLE, self.H_TABLE):
                    in_pocket.append(ID)
            for ID in in_pocket:
                balls.pop(ID)
                pocketed.append(ID)

            if counter % 4 == 0:
                # store this time frame in log
                log.append(copy.deepcopy(balls))
            counter += 1

            # check if all balls have stopped, break if so
            balls_in_motion = 0
            for ID in balls.keys():
                if balls[ID].v[0] != 0.0:
                    balls_in_motion += 1
            if balls_in_motion == 0:
                break

        # once while loop exits, log changes to balls
        self.balls = balls
        self.log = log
        self.pocketed = pocketed
