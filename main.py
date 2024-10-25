from __future__ import annotations

import datetime
import time
import matplotlib.pyplot as plt

from game_logic.game_loop import GameLoop
from src.visualize.visualize import graph_state, open_visualization, animate, animation
from src.input_handler import InputHandler
from src.player.player import PlayerID

class GameSession:

    def __init__(self) -> None:

        self.player_names = [InputHandler.get_name(PlayerID.PLAYER_0),
                        InputHandler.get_name(PlayerID.PLAYER_1)]

        self.game = GameLoop(self.player_names)
        self.game.start_game(time.time())

        start_fig = graph_state(self.game.running_state)
        plt.savefig("start_fig.jpg")
        open_visualization("start_fig.jpg")

        for i, name in enumerate(self.player_names):
            print(f"{name}, your team is {self.game.players[i].team}")


    def play(self) -> None:
        # every turn of the loop will be one turn of the game

        game_over = False
        while not game_over:

            # take input for that player
            print(f"{self.game.current_player_name()}, your turn:")
            velocity = InputHandler.get_velocity()
            angle = InputHandler.get_angle()


            # update the state
            self.game.update_state(velocity, angle)

            pocketed = self.game.pocketed_this_turn()

            # update each player's balls left list
            self.game.update_players()

            # output graph
            anim = animate(self.game.running_state.log)
            time = datetime.datetime.now()
            file = f"{time.month}-{time.day}--{time.hour}-{time.minute}-{time.second}--graphic"
            video_writer = animation.FFMpegWriter(fps=24)
            print("Game is being animated")
            anim.save(file + ".mp4", writer=video_writer)

            last_state = graph_state(self.game.running_state)

            plt.savefig(file + ".jpg")
            open_visualization(file + ".jpg")

            open_visualization(file + ".mp4")

            print(f"The balls pocketed this turn were {*pocketed,}")

            # end of game logic
            if 8 in pocketed:
                print(f"Game over! {self.game.winner()} wins!")
                break

            # figure out who plays next
            self.game.current_player_id = self.game.next_player(pocketed)




if __name__ == "__main__":
    game_session = GameSession()
    game_session.play()