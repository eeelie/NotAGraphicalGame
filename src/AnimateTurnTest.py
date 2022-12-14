from visualize import animate
from StartGame import start_game
from ball import Ball
from game import *
from state import State
import datetime
from copy import deepcopy

state_curr = []
game = Game("Jack","Hayden")
game.start_game()
state_curr += [game.running_state.balls]
for i in range(5):
    # balls = deepcopy(state_curr[i])
    # cue = balls[0]
    # balls[0].p[1] = cue.p[1] + 0.625
    #balls[0] = Ball(cue.ID, cue.radius, cue.p[0], cue.p[1] + 0.0625, cue.v[0], cue.v[1])
    game.update_state(2, 0)
    print(game.running_state.balls[0].p)
    state_curr += [game.running_state.balls]

# for balls in state_curr:
#     print(balls[0])
anim = animate(state_curr)

time = datetime.datetime.now()
file_name = f"{time.month}-{time.day}--{time.hour}-{time.minute}-{time.second}--animation.gif"
anim.save(file_name)

