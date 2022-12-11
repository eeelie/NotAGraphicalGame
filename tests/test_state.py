from ball import Ball
from state import State
from state import find_collision_angle
from pytest import approx
from pytest import raises
import numpy as np

RADIUS = 0.05715/2
balls = {
    0: Ball(0,RADIUS,0,0,0,0),
    1: Ball(1,RADIUS,0.2,0,0,0),
    2: Ball(2,RADIUS,0.2,0.2,0,0),
    3: Ball(3,RADIUS,0,0.2,0,0),
    4: Ball(4,RADIUS,-0.2,0.2,0,0),
    5: Ball(5,RADIUS,-0.2,0,0,0),
    6: Ball(6,RADIUS,-0.2,-0.2,0,0),
    7: Ball(7,RADIUS,0,-0.2,0,0),
    8: Ball(8,RADIUS,0.2,-0.2,0,0)
}

def test_constructor():
    S = State(balls)
    assert S.balls == balls
    assert S.balls[0] == Ball(0,RADIUS,0,0,0,0)

def test_find_collision_angle():
    assert find_collision_angle(balls[0].p, balls[1].p) == approx(-np.pi/2)
    assert find_collision_angle(balls[0].p, balls[2].p) == approx(-np.pi/4)
    assert find_collision_angle(balls[0].p, balls[3].p) == approx(0)
    assert find_collision_angle(balls[0].p, balls[4].p) == approx(np.pi/4)
    assert find_collision_angle(balls[0].p, balls[5].p) == approx(np.pi/2)
    assert find_collision_angle(balls[0].p, balls[6].p) == approx(-5*np.pi/4)
    assert find_collision_angle(balls[0].p, balls[7].p) == approx(-np.pi)
    assert find_collision_angle(balls[0].p, balls[8].p) == approx(-3*np.pi/4)
    
def test_collision_confirmed():
    ...
    
def test_update():
    ...