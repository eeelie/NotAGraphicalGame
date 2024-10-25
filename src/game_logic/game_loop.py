
from __future__ import annotations
import random
import dataclasses
from src.player.player import Player, PlayerID
from src.ball.ball import Ball
from game_logic.team import Team
from game_logic.game_state import GameState
from src.game_logic.start_positions import BALL_START_POSITIONS

@dataclasses.dataclass
class GameLoop():
    players: list[Player, Player]
    running_state: GameState
    current_player_id: PlayerID
    
    def __init__(self, player_names:list[str]):
        self.players = [Player(player_names[0], 0), Player(player_names[1], 1)]
        self.current_player_id = PlayerID.random()
        
    def start_game(self, rand_seed: int = 1) -> GameState:
        ''' sets up the start of the game '''
        BALL_RAD = 0.05715/2
        random.seed(rand_seed)
        ball_start_positions = BALL_START_POSITIONS
        eight_pos = ball_start_positions.pop(4)
        cue_pos = (0, -0.635)
        
        # randomize ball positions
        random.shuffle(ball_start_positions)

        # create ball objects
        game_balls = {}
        i = 0
        for coords in ball_start_positions:
            if i == 0:
                game_balls[i] = Ball(i, BALL_RAD, cue_pos[0], cue_pos[1], 0, 0)
                i += 1
            elif i == 8:
                game_balls[i] = Ball(i, BALL_RAD, eight_pos[0], eight_pos[1], 0, 0)
                i += 1

            game_balls[i] = Ball(i, BALL_RAD, coords[0], coords[1], 0, 0)
            i += 1
            
        # assign a team to each player
        teams = [Team.STRIPED, Team.SOLID]
        random.shuffle(teams)
        for player in self.players:
            player.assign_team(teams.pop())
        
        # starting a state object
        initial_state = GameState(game_balls)
        self.running_state = initial_state
        
    def current_player_name(self) -> str:
        ''' returns the current player's name '''
        return self.players[self.current_player_id].name
    
    def update_state(self, velocity: float, angle: float):
        ''' updates the running state '''
        self.running_state.update(velocity, angle)
        
    def pocketed_this_turn(self) -> list[int]:
        ''' return the list of pocketed balls this turn'''
        return self.running_state.pocketed
    
    def update_players(self):
        ''' updates each player's balls left list '''
        for i in range(2):
            self.players[i].update_balls_left(self.running_state.pocketed)
            
    def winner(self) -> str:
        ''' called if 8 ball is pocketed, returns id of the winner '''
        if self.players[self.current_player_id].down_to_the_eight:
            if 0 not in self.pocketed_this_turn():
                return  self.players[self.current_player_id].name
            else:
                return self.players[Player.get_opponent_id(self.current_player_id)].name                
        else:
            return self.players[Player.get_opponent_id(self.current_player_id)].name  
        
    
    def next_player(self, pocketed: list[int]) -> int:
        """
        To be ran at the end of each turn of the loop, updates current_player_id
        can assume the first ball pocketed wasnt the eight ball, as pocketing the eight always ends the game
        check for the eight before running this function
        """
        # if 8 ball is pocketed, we should never get here, see GameSession.play()
        if 8 in pocketed:
            raise Exception("First ball cannot be the eight ball")

        #no balls pocketed
        if len(pocketed) == 0:
            return Player.get_opponent_id(self.current_player_id)

        # cue pocket scratch
        if 0 in pocketed:
            return Player.get_opponent_id(self.current_player_id)

        # wrong ball scratch
        first_ball_team = Team.from_id(pocketed[0])
        if self.players[self.current_player_id].team != first_ball_team:
            return Player.get_opponent_id(self.current_player_id)
        
        # else case: if the self.players[current_player_id].team == first_ball_team, 
        # then keep current-player the same
        return self.current_player_id
