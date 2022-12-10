
import matplotlib.pyplot as plt

from BallClass import Ball

# Get Ball Color for Plot
def getBallColor(ball: Ball) -> str:
    colors = {0: "white", 1: "yellow", 2: "blue", 3: "red", 4: "purple", 5: "darkorange",6: "limegreen", 7: "brown", 8: "black", 9: "yellow", 10: "blue", 11: "red", 12: "purple", 13: "darkorange", 14: "limegreen", 15: "brown"}

    return colors.get(ball.ID)

def graph_state(balls):
    # Create Plot
    W_TABLE = 1.27
    H_TABLE = 2.54
    fig, ax = plt.subplots(figsize=(W_TABLE*4,H_TABLE*4))
    plt.rcParams["hatch.linewidth"] = 4

    ax.margins(0.3)
    ax.set_facecolor("green")
    ax.set_ylim(-H_TABLE/2, H_TABLE/2)
    ax.set_xlim(-W_TABLE/2, W_TABLE/2)

    for ball in balls.values():
         color = getBallColor(ball)

         if ball.team == "stripe":
             plotBall = plt.Circle(ball.p, ball.radius, facecolor= color, edgecolor ="white", hatch =r"-")
         else:
             plotBall = plt.Circle(ball.p, ball.radius, facecolor= color, edgecolor ="white")

         ax.add_patch(plotBall)

    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    plt.show()

