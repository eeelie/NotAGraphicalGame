
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from ball import Ball
from state import State
from functools import partial

def animate(balls_to_graph: list[dict[int: Ball]]):
    # Create Plot
    W_TABLE = 1.27
    H_TABLE = 2.54
    fig, ax = plt.subplots(figsize=(W_TABLE*4,H_TABLE*4))
    plt.rcParams["hatch.linewidth"] = 4

    ax.margins(0.3)
    ax.set_facecolor("green")
    ax.set_ylim(-H_TABLE/2, H_TABLE/2)
    ax.set_xlim(-W_TABLE/2, W_TABLE/2)

    def init():
        ball_patches = []
        return []

    def graph(i, ball_log: list[dict[int: Ball]]):
        for circle in ax.findobj(match = type(ax.add_patch(plt.Circle((0,0), 5)))):
            circle.remove()
        ball_patches = []

        balls = ball_log[i]
        for ball in balls.values():
            color = getBallColor(ball)
            ball_patches = []

            if ball.team == "stripe":
                plotBall = plt.Circle(ball.p, ball.radius, facecolor= color, edgecolor ="white", hatch =r"-")
            else:
                plotBall = plt.Circle(ball.p, ball.radius, facecolor= color, edgecolor ="white")

            ball_patches += [ax.add_patch(plotBall)]

        return ball_patches

    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    anim = animation.FuncAnimation(fig, partial(graph, ball_log=balls_to_graph), init_func=init, frames=len(balls_to_graph), interval=100, blit=True)


    return anim

# Get Ball Color for Plot
def getBallColor(ball: Ball) -> str:
    colors = {0: "white", 1: "yellow", 2: "blue", 3: "red", 4: "purple", 5: "darkorange",6: "limegreen", 7: "brown", 8: "black", 9: "yellow", 10: "blue", 11: "red", 12: "purple", 13: "darkorange", 14: "limegreen", 15: "brown"}

    return colors.get(ball.ID)

def graph_state(state: State):
    # Create Plot
    W_TABLE = 1.27
    H_TABLE = 2.54
    fig, ax = plt.subplots(figsize=(W_TABLE*2,H_TABLE*2))
    plt.rcParams["hatch.linewidth"] = 4

    ax.margins(0.3)
    ax.set_facecolor("green")
    ax.set_ylim(-H_TABLE/2, H_TABLE/2)
    ax.set_xlim(-W_TABLE/2, W_TABLE/2)

    for ball in state.balls.values():
         color = getBallColor(ball)

         if ball.team == "stripe":
             plotBall = plt.Circle(ball.p, ball.radius, facecolor= color, edgecolor ="white", hatch =r"-")
         else:
             plotBall = plt.Circle(ball.p, ball.radius, facecolor= color, edgecolor ="white")

         ax.add_patch(plotBall)

    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    plt.show()





