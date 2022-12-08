
import dataclasses
from BallClass.py import Ball
import math


def collision_confirmed(p_ay: float, p_by: float, v_ay: float, v_by: float) -> bool:
    "this is a simple helper function to take the transformed y positionas and velocity"
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


def find_collision_angle(p_a: list[float, float], p_b: list[float, float]) -> float:
    "calculates angle of tangent plane in between two colliding balls, in radians"
    "should return a value in [-pi/2, pi/2]"

    if (p_a[0] == p_b[0]) : 
        return 0
    else:
        angle_of_contact = math.atan((p_a[0]-p_b[0])/(p_a[1]-p_b[1]))
        if angle_of_contact > 0 : return angle_of_contact - (math.pi/2)
        if angle_of_contact < 0 : return angle_of_contact + (math.pi/2)
    

@dataclasses.dataclass
class State():
    balls: dict          # dictionary of all balls in play, keyed by ID
    W_TABLE: 1.27        # meters
    H_TABLE: 2.54        # meters
    BALL_RADIUS: 0.5715  # meters
    dt: 0.01             # seconds
    
    def __init__(self, initial_balls: dict[int: Ball]):
        self.balls = initial_balls

    def update(self, velocity: float, degrees: float):
        
        "provides input to cue ball and manages interactions"
        balls = self.balls
        
        # provide input to cue ball
        if 0 not in balls: raise Exception("Cue ball not in play")
        balls[0].v = [velocity, math.radians(degrees)]
        
        # keep track of balls in motion
        balls_in_motion = []
        for i in range(len(balls)):
            if balls[balls.keys()[i]].v[0] != 0.0: balls_in_motion.append(balls.keys()[i])
        
        while len(balls_in_motion) > 0:

            new_balls_in_motion = []

            # run through every moving ball
            for ID in balls_in_motion:
                moving_ball = balls[ID]
                
                # step ball forward (update position and velocity)
                moving_ball.time_step(self.dt)
                
                # check for collisions with all other balls and modify velocities if necessary
                for i in range(len(balls)):
                    other_ID = balls.keys()[i]
                    other = balls[other_ID]
                    
                    if (ID != other_ID) and moving_ball.collides_with(other):
                        # pulling position and velocity out
                        p_a = balls[ID].p
                        p_b = balls[other_ID].p
                        v_a = balls[ID].v
                        v_b = balls[other_ID].v
                        
                        # performing rotation on velocity and decomposing
                        collision_angle = find_collision_angle(p_a, p_b)
                        v_a[1] -= collision_angle
                        v_b[1] -= collision_angle
                        
                        v_ax = v_a[0]*math.sin(v_a[1])
                        v_ay = v_a[0]*math.cos(v_a[1])
                        v_bx = v_b[0]*math.sin(v_b[1])
                        v_by = v_b[0]*math.cos(v_b[1])
                        
                        # checking if the overlapping balls actually hit each other
                        p_ay = p_a[0]*math.sin(collision_angle)+p_a[1]*math.cos(collision_angle)
                        p_by = p_b[0]*math.sin(collision_angle)+p_b[1]*math.cos(collision_angle)
                        
                        if collision_confirmed(p_ay, p_by, v_ay, v_by):
                            # change velocities of both balls
                            v_a_new = (v_ax**2 + v_by**2)**0.5
                            v_b_new = (v_bx**2 + v_ay**2)**0.5
                            theta_a_new = math.atan(v_by/v_ax) + collision_angle
                            theta_b_new = math.atan(v_ay/v_bx) + collision_angle
                            
                            moving_ball.v = [v_a_new, theta_a_new]
                            other.v = [v_b_new, theta_b_new]
                            
                            # add modified balls back into dict
                            balls[ID] = moving_ball
                            balls[other_ID] = other
                        
                        # add other to new_balls_in_motion if necessary
                        if other_ID not in balls_in_motion:
                            new_balls_in_motion.append(other_ID)
                        
                # check for table collisions and modify velocity if necessary
                if moving_ball.collides_with_table(self.W_TABLE, self.H_TABLE):
                    v_x = moving_ball.v[0]*math.cos(moving_ball.v[1])
                    v_y = moving_ball.v[0]*math.sin(moving_ball.v[1])

                    if (moving_ball.p[0]+moving_ball.radius >= self.W_TABLE/2) and (v_x > 0):
                        v_x = -v_x
                    elif (moving_ball.p[0]-moving_ball.radius <= -self.W_TABLE/2) and (v_x < 0):
                        v_x = -v_x
                    elif (moving_ball.p[1]+moving_ball.radius >= self.H_TABLE/2) and (v_y > 0):
                        v_y = -v_y
                    elif (moving_ball.p[1]-moving_ball.radius <= -self.H_TABLE/2) and (v_y < 0):
                        v_y = -v_y

                    moving_ball.v[0] = (v_x**2 + v_y**2)**0.5
                    moving_ball.v[1] = math.atan(v_x/v_y)
                    balls[ID] = moving_ball
                
                # check for pockets
                if moving_ball.in_pocket(self.W_TABLE, self.H_TABLE):
                    balls_in_motion.pop(ID)
                    balls.pop(ID)
                
            # add any collided balls to balls_in_motion as necessary
            balls_in_motion.append(new_balls_in_motion)

            # if any ball's velocity is sufficiently low, remove from balls_in_motion
            for ID in balls_in_motion:
                if balls[ID].v[0] <= 0.001:
                    balls[ID].v[0] = 0.0
                    balls_in_motion.pop(ID)

        # once while loop exits, log changes to balls
        self.balls = balls
                        

    def reset_cue_ball(self):
        "brings cue ball back into play by setting it at the break spot"

        if 0 in self.balls: raise Exception("Cue ball already in play")
        else: self.balls[0] = Ball(0, self.BALL_RADIUS, 0, -self.H_TABLE/2, 0, 0)
        
