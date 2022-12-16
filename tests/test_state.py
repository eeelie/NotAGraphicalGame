
from ball import Ball
from state import *
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
    assert S.balls[0].p[0] == 0

def test_modify_simulation_constants():
    S = State(balls)
    S.modify_simulation_constants(0.02, 0.015, 0.8)
    assert S.DT == approx(0.02)
    assert S.ACCELERATION == approx(0.015)
    assert S.WALL_DAMPENING == approx(0.8)
    
def test_find_collision_angle():
    assert find_collision_angle(balls[0].p, balls[1].p) == approx(-np.pi/2)
    assert find_collision_angle(balls[0].p, balls[2].p) == approx(-np.pi/4)
    assert find_collision_angle(balls[0].p, balls[3].p) == approx(0)
    assert find_collision_angle(balls[0].p, balls[4].p) == approx(np.pi/4)
    assert find_collision_angle(balls[0].p, balls[5].p) == approx(np.pi/2)
    assert find_collision_angle(balls[0].p, balls[6].p) == approx(-5*np.pi/4)
    assert find_collision_angle(balls[0].p, balls[7].p) == approx(-np.pi)
    assert find_collision_angle(balls[0].p, balls[8].p) == approx(-3*np.pi/4)
    
def test_rotate_p_and_v():
    p_new, v_new = rotate_p_and_v([1,0], [5, np.pi/2], np.pi/4)
    assert p_new[0] == approx(np.sqrt(2)/2)
    assert p_new[1] == approx(-np.sqrt(2)/2)
    assert v_new[0] == 5
    assert v_new[1] == np.pi/4
    
    
def test_collision_confirmed():
    # balls headed away from each other
    assert collision_confirmed(1, -1, 1, -1) == False
    assert collision_confirmed(-1, 1, -1, 1) == False
    # one faster than other, headed up
    assert collision_confirmed(1, -1, 2, 1) == False
    assert collision_confirmed(-1, 1, 1, 2) == False
    # one faster than other, headed down
    assert collision_confirmed(1, -1, -1, -2) == False
    assert collision_confirmed(-1, 1, -2, -1) == False
    # true collisions
    assert collision_confirmed(1, -1, -1, 1) == True
    assert collision_confirmed(1, -1, -2, -1) == True
    assert collision_confirmed(1, -1, 1, 2) == True
    assert collision_confirmed(-1, 1, 1, -1) == True
    assert collision_confirmed(-1, 1, 2, 1) == True
    assert collision_confirmed(-1, 1, -1, -2) == True
    
def test_collision_confirmed_integrated():
    ball_a = Ball(1,RADIUS,0,-3,5,0)
    ball_b = Ball(2,RADIUS,2,-2,5,3*np.pi/2)
    
    collision_angle = find_collision_angle(ball_a.p, ball_b.p)
    p_a, v_a = rotate_p_and_v(ball_a.p, ball_a.v, collision_angle)
    p_b, v_b = rotate_p_and_v(ball_b.p, ball_b.v, collision_angle)
    v_ay = v_a[0]*np.sin(v_a[1])
    v_by = v_b[0]*np.sin(v_b[1])
                        
    assert collision_confirmed(p_a[1], p_b[1], v_ay, v_by) == True
    
def test_post_collision_velocities():
    v_ax = 4
    v_ay = 5
    v_bx = 12
    v_by = -3
    collision_angle = np.pi/4
    v_a1, v_b1 = post_collision_velocities(v_ax, v_ay, v_bx, v_by, collision_angle)
    theta_a1 = np.arctan2(-3, 4) + collision_angle
    theta_b1 = np.arctan2(5, 12) + collision_angle
    assert v_a1[0] == approx(5)
    assert v_b1[0] == approx(13)
    assert v_a1[1] == approx(theta_a1)
    assert v_b1[1] == approx(theta_b1)
    
    v_ax = np.sqrt(3)/2
    v_ay = np.sqrt(2)/2
    v_bx = -np.sqrt(2)/2
    v_by = -1/2
    v_a2, v_b2 = post_collision_velocities(v_ax, v_ay, v_bx, v_by, 0)
    v_a3, v_b3 = post_collision_velocities(v_ax, v_ay, v_bx, v_by, collision_angle)
    assert v_a2[1] == approx(-np.pi/6)
    assert v_b2[1] == approx(3*np.pi/4)
    assert v_a3[1] == approx(np.pi/12)
    assert v_b3[1] == approx(np.pi)
    
def test_update_reset_cue():
    balls_no_cue = {
        1: Ball(1,RADIUS,0.2,0,0,0),
        2: Ball(2,RADIUS,0.2,0.2,0,0)
    }
    S = State(balls_no_cue)
    S.update(0,0)
    assert 0 in S.balls.keys()
    
def test_update_simple():
    S = State(balls)
    S.update(1, 0)
    assert 0 in S.balls.keys()
    assert 1 not in S.balls.keys()
    assert S.pocketed == [1]
