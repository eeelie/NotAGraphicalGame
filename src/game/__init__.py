
from __future__ import annotations
import random
import dataclasses
from player import *

#what team is ball number ID?    
def ball_team(ID: int):
    assert ID >= 0 and ID <= 15, "Not a valid ball ID."

    if ID >= 1 and ID <= 7:
        return "solids"
    elif ID >= 9 and ID <= 15:
        return "stripes"
    elif ID == 8:
        return "eight"
    elif ID == 0:
        return "cue"  


def other_player(this_player: int) -> int:
    '''
    returns the id of the other player
    '''
    assert this_player == 0 or this_player == 1, "not a valid player ID"
    
    if this_player == 0:
        return 1
    if this_player == 1:
        return 0

@dataclasses.dataclass
class Game():
    '''
    Assuming I can receive a list of balls pocketed from State
    and the dict with all balls still in play, which shouldnt be necessary
    '''
    players: list[Player, Player]
    current_player_id: int #0 or 1
    
    def __init__(self, player1: Player, player2: Player):        
        self.players = [player1, player2]
        self.current_player_id = random.randint(0,1)    

        
    def start_game(self) -> State:
        BALL_RAD = 0.05715/2
        standard_ball_positions = [(0, 0.635), (-0.0286, 0.6846), (0.0288, 0.6848), (-0.0572, 0.7342), (0.00020, 0.7344), (0.0576, 0.7346), (-0.0858, 0.7838), (-0.0284, 0.784), (0.0289, 0.7842), (0.0864, 0.7844), (-0.1144, 0.8334), (-0.057, 0.8336), (0.0004, 0.8338), (0.0578, 0.834), (0.1152, 0.8342)]        
        eight_pos = standard_ball_positions.pop(4)
        cue_pos = (0, -0.635)
        
        # randomize ball positions
        random.shuffle(standard_ball_positions)

        # create ball objects
        game_balls = {}
        i = 0
        for coords in standard_ball_positions:
            if i == 0:
                game_balls[i] = Ball(i, BALL_RAD, cue_pos[0], cue_pos[1], 0, 0)
                i += 1
            elif i == 8:
                game_balls[i] = Ball(i, BALL_RAD, eight_pos[0], eight_pos[1], 0, 0)
                i += 1

            game_balls[i] = Ball(i, BALL_RAD, coords[0], coords[1], 0, 0)
            i += 1
            
        # assign a team to each player
        teams = ["stripes", "solids"]
        random.shuffle(teams)
        for i in range(2):
            self.players[i].assign_team(teams[i])
            #print(self.players[i].balls_left)
        
        # starting a state object and graphing it
        initial_state = State(game_balls)
        graph_state(initial_state)
        return initial_state       
    
    
    def next_player(self, pocketed: list[int]) -> int:
        """
        To be ran at the end of each turn of the loop, updates current_player_id
        can assume the first ball pocketed wasnt the eight ball, as pocketing the eight always ends the game
        check for the eight before running this function
        
        might break if we somehow get in here and first_ball_team == "eight"
        """
        
        #no balls pocketed
        if len(pocketed) == 0:
            return other_player(self.current_player_id)
            
        first_ball_team = ball_team(pocketed[0])
                   
        # cue pocket scratch
        if 0 in pocketed:
            return other_player(self.current_player_id)
        
        # wrong ball scratch
        if self.players[self.current_player_id].team != first_ball_team:
            return other_player(self.current_player_id)
        
        # else case: if the self.players[current_player_id].team == first_ball_team, 
        # then keep current-player the same
        return self.current_player_id
