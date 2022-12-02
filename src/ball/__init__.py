import dataclasses


@dataclasses.dataclass
class Ball():
    ID: int 
    radius: float
    pocket: bool
    p: list[float, float]
    v: list[float, float]
        
    def __init__(self, ID: int, radius: float, x_0: float, y_0: float, vx_0: float, vy_0: float):
        self.ID = ID
        self.radius = radius
        self.pocket = False
        self.p = [x_0,y_0]
        self.v = [vx_0,vy_0]
        
    def time_step(self, dx):
        ACCELERATION = - 0.1 # meters/second^2
        "steps forward position and velocity of ball"
        p_new = [self.p[0] + self.v[0]*dx + 0.5*ACCELERATION*dx*dx, self.p[1] + self.v[1]*dx + 0.5*ACCELERATION*dx*dx]
        v_new = [self.v[0]+ACCELERATION*dx, self.v[1]+ACCELERATION*dx]
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
