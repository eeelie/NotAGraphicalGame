import dataclasses
import numpy as np

@dataclasses.dataclass
class Ball():
    ID: int
    radius: float
    pocket: bool
    p: list[float, float]
    v: list[float, float]
    team: str
        
    def __init__(self, ID: int, radius: float, x_0: float, y_0: float, v_mag: float, v_dir: float):
        self.ID = ID
        self.radius = radius
        self.pocket = False
        self.p = [x_0,y_0]
        self.v = [v_mag,v_dir]
        self.team = self.team_name()
       
    def team_name(self):
        assert self.ID >= 0 and self.ID <= 15, "Not a valid ball ID."
        
        if self.ID >= 1 and self.ID <= 7:
            return "solid"
        elif self.ID >= 9 and self.ID <= 15:
            return "stripe"
        elif self.ID == 8:
            return "eight"
        elif self.ID == 0:
            return "cue"

    def time_step(self, dt):
        ACCELERATION = - 0.1 # meters/second^2
        "steps forward position and velocity of ball"
        v_x = self.v[0]*np.cos(self.v[1])
        v_y = self.v[0]*np.sin(self.v[1])
        a_x = ACCELERATION * np.cos(self.v[1])
        a_y = ACCELERATION * np.sin(self.v[1])
        p_new = [self.p[0] + v_x*dt + 0.5*a_x*dt*dt, self.p[1] + v_y*dt + 0.5*a_y*dt*dt]
        v_new = [((v_x+a_x*dt)**2+(v_y+a_y*dt)**2)**0.5, self.v[1]]
        return p_new, v_new
    
    def collides_with(self,other) -> bool :
        "returns true if ball is in collision with other ball object"
        dist = ((self.p[0]-other.p[0])**2+(self.p[1]-other.p[1])**2)**0.5
        if dist <= self.radius+other.radius:
            return True
        else:
            return False
    
    def collides_with_table(self, w: float, h: float) -> bool :
        "returns true if ball is touching either an edge or a pocket"
        if self.p[0]+self.radius >= w/2:
            return True
        elif self.p[0]-self.radius <= -w/2:
            return True
        elif self.p[1]+self.radius >= h/2:
            return True
        elif self.p[1]-self.radius <= -h/2:
            return True
        else:
            return False
