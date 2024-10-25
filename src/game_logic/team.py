from enum import Enum

class Team(Enum):
    SOLID = "solid"
    STRIPED = "striped"
    EIGHT = "eight"
    CUE = "cue"
    UNDEFINED = None

    @classmethod
    def from_id(cls, ball_id: int|None):
        if ball_id is None: return cls.UNDEFINED

        if ball_id < 0 or ball_id > 15: raise Exception("Not a valid ball ID.")

        if ball_id == 8:
            return cls.EIGHT
        
        if ball_id == 0:
            return cls.CUE

        if ball_id >= 1 and ball_id <= 7:
            return cls.SOLID
        
        if ball_id >= 9 and ball_id <= 15:
            return cls.STRIPED

    @classmethod
    def get_team_balls(cls, team:"Team") -> list[int]:

        if team is cls.SOLID:
            return [i for i in range(1, 8)] 
        
        if team is cls.STRIPED:
            return [i for i in range(9, 16)]
        
        raise ValueError(f"Invalid team: {team}")
