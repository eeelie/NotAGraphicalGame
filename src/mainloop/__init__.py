
from __future__ import annotations
from game import *
from player import *
from graphstate import *


player1_name = input("Player 1, what's your name?")
player2_name = input("Player 2, what's your name?")

game = Game(Player(player1_name),Player(player2_name))
running_state = game.start_game()

print(f"{player1_name}, your team is {game.players[0].team}")
print(f"{player2_name}, your team is {game.players[1].team}")

def new_input():
    force = float(input("Input a velocity in m/s"))
    angle = float(input("Input an angle in degrees"))
    return force, angle

game_over = False
#every run of the loop will be one turn of the game
while not game_over:        
       
    #take input for that player
    print(f"{game.players[game.current_player_id].name}, your turn:")
    velocity, angle = new_input()

    #update the state
    running_state.update(velocity, angle)

    pocketed = running_state.pocketed
    print(f"pocketed = {pocketed}")

    # update each player's balls left list
    for i in range(2):
        game.players[i].update_balls_left(pocketed)
    
    # output graph
    graph_state(running_state)
    
    # end of game logic
    if 8 in pocketed:
        if game.players[self.current_player_id].down_to_the_eight:
            print(f"Game over! Player {game.current_player_id + 1} wins!")
        else:
            print(f"Game over! Player {game.current_player_id + 1} loses!")
        break

    # figure out who plays next
    game.current_player_id = game.next_player(pocketed)
