
from __future__ import annotations
from game import *
from visualize import *
import datetime

player1_name = input("Player 1, what's your name?")
player2_name = input("Player 2, what's your name?")

game = Game(player1_name,player2_name)
game.start_game()

print(f"{player1_name}, your team is {game.players[0].team}")
print(f"{player2_name}, your team is {game.players[1].team}")

game_over = False
#every run of the loop will be one turn of the game
while not game_over:        
       
    #take input for that player
    print(f"{game.current_player_name()}, your turn:")
    velocity, angle = take_input()

    #update the state
    game.update_state(velocity, angle)

    pocketed = game.pocketed_this_turn()
    

    # update each player's balls left list
    game.update_players()
    
    output graph
    graph_state(game.running_state)
    print(f"number of states to be graphed: {len(game.running_state.log)}")
    anim = animate(game.running_state.log)
    time = datetime.datetime.now()
    file_name = f"{time.month}-{time.day}--{time.hour}-{time.minute}-{time.second}--animation.mp4"
    video_writer = animation.FFMpegWriter(fps=30)
    anim.save(file_name, writer=video_writer)

    open_visualization(file_name)

    print(f"The balls pocketed this turn were {*pocketed,}")
    
    # end of game logic
    if 8 in pocketed:
        print(f"Game over! {game.winner()} wins!")
        break

    # figure out who plays next
    game.current_player_id = game.next_player(pocketed)
