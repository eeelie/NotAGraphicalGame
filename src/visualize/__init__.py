import matplotlib.pyplot as plt
from matplotlib import animation
from ball import Ball
from state import State
from functools import partial
import sys
from typing import Dict


def animate(balls_to_graph: list[Dict[int:Ball]]):
    # Create Plot
    W_TABLE = 1.27
    H_TABLE = 2.54
    fig, ax = plt.subplots(figsize=(W_TABLE * 4, H_TABLE * 4))
    plt.rcParams["hatch.linewidth"] = 4

    ax.margins(0.3)
    ax.set_facecolor("green")
    ax.set_ylim(-H_TABLE / 2, H_TABLE / 2)
    ax.set_xlim(-W_TABLE / 2, W_TABLE / 2)

    def init():
        ball_patches = []
        return []

    def graph(i, ball_log: list[dict[int:Ball]]):
        for circle in ax.findobj(match=type(ax.add_patch(plt.Circle((0, 0), 5)))):
            circle.remove()
        ball_patches = []

        # Adding Pocket References
        ball_patches += [
            ax.add_patch(plt.Circle((1.27 / 2, 2.54 / 2), 0.114, facecolor="gray"))
        ]
        ball_patches += [
            ax.add_patch(plt.Circle((-1.27 / 2, -2.54 / 2), 0.114, facecolor="gray"))
        ]
        ball_patches += [
            ax.add_patch(plt.Circle((1.27 / 2, -2.54 / 2), 0.114, facecolor="gray"))
        ]
        ball_patches += [
            ax.add_patch(plt.Circle((-1.27 / 2, 2.54 / 2), 0.114, facecolor="gray"))
        ]
        ball_patches += [
            ax.add_patch(plt.Circle((1.27 / 2, 0), 0.12 / 2, facecolor="gray"))
        ]
        ball_patches += [
            ax.add_patch(plt.Circle((-1.27 / 2, 0), 0.12 / 2, facecolor="gray"))
        ]

        # Add cue patch
        ax.add_patch(plt.Circle((0, -0.635), 0.02, facecolor="tan"))

        balls = ball_log[i]
        for ball in balls.values():
            color = getBallColor(ball)
            ball_patches = []

            if ball.team == "stripe":
                plotBall = plt.Circle(
                    ball.p, ball.radius, facecolor=color, edgecolor="white", hatch=r"-"
                )
            else:
                plotBall = plt.Circle(
                    ball.p, ball.radius, facecolor=color, edgecolor="white"
                )

            ball_patches += [ax.add_patch(plotBall)]

        return ball_patches

    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    anim = animation.FuncAnimation(
        fig,
        partial(graph, ball_log=balls_to_graph),
        init_func=init,
        frames=len(balls_to_graph),
        interval=100,
        blit=True,
    )

    return anim


# Get Ball Color for Plot
def getBallColor(ball: Ball) -> str:
    colors = {
        0: "white",
        1: "yellow",
        2: "blue",
        3: "red",
        4: "purple",
        5: "darkorange",
        6: "limegreen",
        7: "brown",
        8: "black",
        9: "yellow",
        10: "blue",
        11: "red",
        12: "purple",
        13: "darkorange",
        14: "limegreen",
        15: "brown",
    }

    return colors.get(ball.ID)


def graph_state(state: State):
    # Create Plot
    W_TABLE = 1.27
    H_TABLE = 2.54
    fig, ax = plt.subplots(figsize=(W_TABLE * 4, H_TABLE * 4))
    plt.rcParams["hatch.linewidth"] = 4

    ax.margins(0.1)
    ax.set_facecolor("green")
    ax.set_ylim(-H_TABLE / 2, H_TABLE / 2)
    ax.set_xlim(-W_TABLE / 2, W_TABLE / 2)

    # Adding Pocket References
    ax.add_patch(plt.Circle((1.27 / 2, 2.54 / 2), 0.114, facecolor="gray"))
    ax.add_patch(plt.Circle((-1.27 / 2, -2.54 / 2), 0.114, facecolor="gray"))
    ax.add_patch(plt.Circle((1.27 / 2, -2.54 / 2), 0.114, facecolor="gray"))
    ax.add_patch(plt.Circle((-1.27 / 2, 2.54 / 2), 0.114, facecolor="gray"))
    ax.add_patch(plt.Circle((1.27 / 2, 0), 0.12 / 2, facecolor="gray"))
    ax.add_patch(plt.Circle((-1.27 / 2, 0), 0.12 / 2, facecolor="gray"))

    for ball in state.balls.values():
        color = getBallColor(ball)

        if ball.team == "stripe":
            plotBall = plt.Circle(
                ball.p, ball.radius, facecolor=color, edgecolor="white", hatch=r"-"
            )
        else:
            plotBall = plt.Circle(
                ball.p, ball.radius, facecolor=color, edgecolor="white"
            )

        ax.add_patch(plotBall)

    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    return fig


def open_visualization(file_name: str):
    if sys.platform == "win32":
        from os import startfile as open_plot

        open_plot(file_name)
    else:
        import subprocess as open_file

        video_open = "open" if sys.platform == "darwin" else "xdg-open"
        open_file.call([video_open, file_name])
