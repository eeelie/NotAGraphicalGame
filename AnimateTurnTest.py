from AnimateTurn import animate
from StartGame import start_game
from BallClass import Ball
from StateClass import State
from PIL import Image
from PIL import GifImagePlugin
from IPython import display

state_curr = []
state_curr += [start_game()]
for i in range(20):
    balls = state_curr[i].balls.copy()
    cue = balls[0]
    balls[0] = Ball(cue.ID, cue.radius, cue.p[0], cue.p[1] + 0.0625, cue.v[0], cue.v[1])
    state_curr += [State(balls)]

anim = animate(state_curr)

#vid = anim.to_html5_video()
