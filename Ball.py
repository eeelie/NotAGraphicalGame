
import numpy as np
from __future__ import annotations
from collections.abc import Callable


# Ball class

class Ball():
    position: tuple[float, float]
    velocity: tuple[float,float]
    mass: float
    team: str

    def __init__(self, p_0: tuple[float,float], v_0: tuple[float,float], mass: float, team: str):
        position = (p_0[0],p_0[1])
        velocity = (v_0[0],v_0[1])
        mass = mass
        team = team
        
    ''' does a ball colliding with another ball behavie differently than a ball colliding with the table?
    if not, we can have just one collision function
    
    
    I also don't know what the best way to model the ball, initially assuming 2d position and velocity vectors'''    
        
        
    #collision with another ball --> is this actually the same as collision with the table?
    def ballCollision(self, other: Ball, angle: float) -> Ball:
        new_x  = ... # physics!
        new_y  = ... # perpendicular physics!
        new_vx = ... # derivative physics!
        new_vy = ... # perpendicular derivative physics!
        return self.__class__((new_x,new_y), (new_vx,new_vy), self.mass, self.team)
    
    
    #collision with the wall
    def wallCollision(self, angle: float) -> Ball:
        new_x = ... # physics!
        new_y = ... # perpendicular physics!
        new_vx = ... # derivative physics!
        new_vy = ... # perpendicular derivative physics!
        return self.__class__((new_x,new_y), (new_vx,new_vy), self.mass, self.team)
        

