from __future__ import annotations
import dataclasses
from enum import Enum
from random import randint

from game_logic.team import Team

class PlayerID(Enum):
    PLAYER_0 = 0
    PLAYER_1 = 1

    @classmethod
    def random(cls):
        return cls(randint(0,1))

@dataclasses.dataclass
class Player:

    def __init__(self, name: str, player_id:int):
        self.id = PlayerID(player_id)
        self.name = name
        self.team = Team(None)
        self.balls_left = []
        self.down_to_the_eight = False

    def assign_team(self, team: str) -> None:
        """
        Initializes the balls_left list when the teams are assigned
        """
        if team not in [Team.STRIPED, Team.SOLID]:
            raise Exception("Not a valid team.")

        self.team = team

        self.balls_left = Team.get_team_balls(self.team)

    def update_balls_left(self, pocketed: list[int]):

        for i in range(len(pocketed)):
            if pocketed[i] in self.balls_left:
                self.balls_left.remove(pocketed[i])

        # if a player runs out of balls they are now down to the eight
        if len(self.balls_left) == 0:
            self.down_to_the_eight = True

    @classmethod
    def get_opponent_id(cls, current_player: PlayerID) -> int:
        if current_player not in PlayerID: raise Exception("not a valid player ID")    
        
        if current_player is PlayerID.PLAYER_0:
            return PlayerID.PLAYER_1
        if current_player == PlayerID.PLAYER_1:
            return PlayerID.PLAYER_0
