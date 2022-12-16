from __future__ import annotations
import dataclasses
from ball import Ball
import numpy as np
import copy


def find_collision_angle(p_a: list[float, float], p_b: list[float, float]) -> float:
    "calculates angle of tangent plane in between two colliding balls, in radians"
    "should return a value in [-3pi/2, pi/2]"

    angle_of_contact = np.arctan2((p_b[1] - p_a[1]), (p_b[0] - p_a[0]))
    return angle_of_contact - (np.pi / 2)


def rotate_p_and_v(p: list[float, float], v: list[float, float], theta_radians: float):
    "performs simple rotation on velocity [magnitude, direction] and position [x,y]"
    "theta_radians is the collision angle, or the angle of the new frame w.r.t 0"

    v_theta_new = v[1] - theta_radians
    p_x = p[0] * np.cos(-theta_radians) - p[1] * np.sin(-theta_radians)
    p_y = p[0] * np.sin(-theta_radians) + p[1] * np.cos(-theta_radians)
    return [p_x, p_y], [v[0], v_theta_new]


def collision_confirmed(p_ay: float, p_by: float, v_ay: float, v_by: float) -> bool:
    "this is a simple helper function to take the rotated y positions and velocity"
    "of two colliding balls and confirm that they are going to hit each other"

    if (p_ay < p_by) and (v_ay < 0) and (v_by > 0):
        return False
    elif (p_ay > p_by) and (v_ay > 0) and (v_by < 0):
        return False
    elif (p_ay < p_by) and (v_ay < v_by < 0):
        return False
    elif (p_by < p_ay) and (v_by < v_ay < 0):
        return False
    elif (p_ay > p_by) and (v_ay > v_by > 0):
        return False
    elif (p_by > p_ay) and (v_by > v_ay > 0):
        return False
    else:
        return True


def post_collision_velocities(
    v_ax: float, v_ay: float, v_bx: float, v_by: float, collision_angle: float
):
    "takes the rotated velocities of colliding balls in x and y components with respect to"
    "the collision plane (at angle = collision_angle), returns v of each ball in [mag, theta]"
    "returns a value between -pi/2 and 3pi/2"

    v_a_new = (v_ax**2 + v_by**2) ** 0.5
    v_b_new = (v_bx**2 + v_ay**2) ** 0.5
    theta_a_new = np.arctan2(v_by, v_ax) + collision_angle
    theta_b_new = np.arctan2(v_ay, v_bx) + collision_angle
    return [v_a_new, theta_a_new], [v_b_new, theta_b_new]


def update_one_step(
    balls: dict, dt: float, acc: float, w: float, h: float, damp: float
) -> dict:
    "takes balls dict and updates every ball one time step, managing collisions"
    "does not check pockets or remove any balls from the dict"

    # run through every ball
    for ID in balls.keys():
        moving_ball = balls[ID]

        # only run on moving balls
        if moving_ball.v[0] == 0.0:
            continue

        # step ball forward (update position and velocity)
        moving_ball.time_step(dt, acc)
        if moving_ball.v[0] == 0.0:
            continue

        # check for collisions with all other balls and modify velocities if necessary
        for i in range(len(balls)):
            other_ID = list(balls.keys())[i]
            other = balls[other_ID]

            if (ID != other_ID) and moving_ball.collides_with(other):
                # pulling position and velocity out
                p_a = balls[ID].p
                p_b = balls[other_ID].p
                v_a = balls[ID].v
                v_b = balls[other_ID].v

                # performing rotation on positions and velocities
                collision_angle = find_collision_angle(p_a, p_b)
                p_a, v_a = rotate_p_and_v(p_a, v_a, collision_angle)
                p_b, v_b = rotate_p_and_v(p_b, v_b, collision_angle)

                # decomposing velocity in new frame of reference
                v_ax = v_a[0] * np.cos(v_a[1])
                v_ay = v_a[0] * np.sin(v_a[1])
                v_bx = v_b[0] * np.cos(v_b[1])
                v_by = v_b[0] * np.sin(v_b[1])
                # checking if the overlapping balls actually hit each other
                if collision_confirmed(p_a[1], p_b[1], v_ay, v_by):

                    # change velocities of both balls
                    moving_ball.v, other.v = post_collision_velocities(
                        v_ax, v_ay, v_bx, v_by, collision_angle
                    )

                    # add modified balls back into dict (this may do nothing)
                    balls[ID] = moving_ball
                    balls[other_ID] = other

        # check for table collisions and modify velocity if necessary
        if moving_ball.collides_with_table(w, h):
            v_x = moving_ball.v[0] * np.cos(moving_ball.v[1])
            v_y = moving_ball.v[0] * np.sin(moving_ball.v[1])

            if (moving_ball.p[0] + moving_ball.radius >= w / 2) and (v_x > 0):
                v_x = -v_x
            elif (moving_ball.p[0] - moving_ball.radius <= -w / 2) and (v_x < 0):
                v_x = -v_x
            elif (moving_ball.p[1] + moving_ball.radius >= h / 2) and (v_y > 0):
                v_y = -v_y
            elif (moving_ball.p[1] - moving_ball.radius <= -h / 2) and (v_y < 0):
                v_y = -v_y

            moving_ball.v[0] = ((v_x**2 + v_y**2) ** 0.5) * damp
            moving_ball.v[1] = np.arctan2(v_y, v_x)
            balls[ID] = moving_ball

    # after updating every ball, return modified balls dict
    return balls


@dataclasses.dataclass
class State:
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
