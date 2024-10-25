from src.player.player import PlayerID

class InputHandler:

    @classmethod
    def get_name(cls, player_id:PlayerID) -> str:
        return input(f"Player {player_id.value}, what is your name?")

    @classmethod
    def get_velocity(cls) -> float:
        return float(input("Input a velocity in m/s"))
        
    @classmethod
    def get_angle(cls) -> float:
        return float(input("Input an angle in degrees"))
