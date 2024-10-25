from src.game_logic.player import PlayerID

class InputHandler:

    @classmethod
    def get_name(cls, player_id:PlayerID) -> str:
        return input(f"Player {player_id.value}, what is your name? ")

    @staticmethod
    def convert_to_float_infinite_retries(func:callable) -> callable:
         
        def wrapper(*args, **kwargs) -> float:
            while True:
                try:
                    str_input = func(*args, **kwargs)
                    float_input = float(str_input) # this will break if the input is invalid
                    return float_input
                except ValueError:
                    print("\nInput must be a valid number!\n")
        
        return wrapper

    @classmethod
    @convert_to_float_infinite_retries
    def get_velocity(cls) -> str:
        return input("Input a velocity in m/s ")
        
    @classmethod
    @convert_to_float_infinite_retries
    def get_angle(cls) -> str:
        return input("Input an angle in degrees ")