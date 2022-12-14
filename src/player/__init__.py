
from __future__ import annotations
import dataclasses

@dataclasses.dataclass
class Player():
    '''
    Player class keeps track of the player's name and team, and the balls they need to pocket to win the game
    '''
    name: str
    team: str
    balls_left: list[int]
    down_to_the_eight: bool
    
    def __init__(self, name: str):
        self.name = name
        self.team = "undefined"
        self.balls_left = [] 
        self.down_to_the_eight = False
        
    # initialize the player's list of balls to pocket and team class variable    
    def assign_team(self, team: str) -> None:
        '''
        Initializes the balls_left list when the teams are assigned
        '''
        if team != "stripes" and team != "solids": raise Exception("Not a valid team.")


        self.team = team
        
        if team == "solids":
            self.balls_left = [i for i in range(1,8)] #all solids
        else:
            self.balls_left = [i for i in range(9,16)] #all stripes
        

    # updates the balls left to win list
    def update_balls_left(self, pocketed: list[int]):
        
        for i in range(len(pocketed)):
            if pocketed[i] in self.balls_left:
                self.balls_left.remove(pocketed[i])
        
        #if a player runs out of balls they are now down to the eight
        if len(self.balls_left) == 0:
            self.down_to_the_eight = True
        
