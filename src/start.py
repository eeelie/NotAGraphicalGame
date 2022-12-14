from game import *
from visualize import *
from LetsPlayPool import *

game = Game("Jose", "Elie")
game.start_game()
print(game.running_state.balls)
graph_state(game.running_state)

