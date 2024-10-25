from __future__ import annotations
import numpy as np
import dataclasses
from enum import Enum

class BallTeam(Enum):
    SOLID = "solid"
    STRIPED = "striped"
    EIGHT = "eight"
    CUE = "cue"

    @classmethod
    def from_id(cls, ball_id: int):
        if ball_id < 0 or ball_id > 15: raise Exception("Not a valid ball ID.")

        if ball_id == 8:
            return cls.EIGHT
        
        if ball_id == 0:
            return cls.CUE

        if ball_id >= 1 and ball_id <= 7:
            return cls.SOLID
        
        if ball_id >= 9 and ball_id <= 15:
            return cls.STRIPED


@dataclasses.dataclass
class Ball:

    def __init__(
        self,
        ball_id: int,
        radius: float,
        x_0: float,
        y_0: float,
        v_mag: float,
        v_radians: float,
    ):
        self.id = ball_id
        self.radius = radius
        self.p = [x_0, y_0]
        self.v = [v_mag, v_radians]
        self.team = BallTeam.from_id(self.id)

    def __copy__(self):
        return Ball(self.id, self.radius, self.p[0], self.p[1], self.v[0], self.v[1])

    def time_step(self, dt: float, acc: float):
        "new implementation: steps forward position and velocity of ball and stops ball if v is suficiently small"
        v_new = self.v[0] - np.absolute(acc) * dt
        if v_new <= 0.001:
            self.v[0] = 0.0
            return
        v_x = v_new * np.cos(self.v[1])
        v_y = v_new * np.sin(self.v[1])
        self.p = [self.p[0] + v_x * dt, self.p[1] + v_y * dt]
        self.v = [v_new, self.v[1]]

    def collides_with(self, other) -> bool:
        "returns true if ball is in collision with other ball object"
        dist = ((self.p[0] - other.p[0]) ** 2 + (self.p[1] - other.p[1]) ** 2) ** 0.5
        if dist <= self.radius + other.radius:
            return True
        else:
            return False

    def collides_with_table(self, w: float, h: float) -> bool:
        "returns true if ball is touching either an edge or a pocket"
        if self.p[0] + self.radius >= w / 2:
            return True
        elif self.p[0] - self.radius <= -w / 2:
            return True
        elif self.p[1] + self.radius >= h / 2:
            return True
        elif self.p[1] - self.radius <= -h / 2:
            return True
        else:
            return False

    def in_pocket(self, w: float, h: float) -> bool:
        "returns true if ball is colliding with table and center is within pocket regions"
        if self.collides_with_table(w, h) == False:
            return False

        SIDE_POCKET_W = 0.127  # m
        CORNER_POCKET_W = 0.114  # m

        if SIDE_POCKET_W / 2 > self.p[1] > -SIDE_POCKET_W / 2:
            return True
        elif h / 2 - CORNER_POCKET_W >= self.p[1] >= CORNER_POCKET_W - h / 2:
            return False
        elif w / 2 - CORNER_POCKET_W >= self.p[0] >= CORNER_POCKET_W - w / 2:
            return False
        else:
            return True
