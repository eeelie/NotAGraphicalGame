
from __future__ import annotations
from game import *
#from graphstate import *

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
    print(f"pocketed = {pocketed}")

    # update each player's balls left list
    game.update_players()
    
    # output graph
    #graph_state(running_state)
    
    # end of game logic
    if 8 in pocketed:
        print(f"Game over! Player {game.winner()} wins!")
        break

    # figure out who plays next
    game.current_player_id = game.next_player(pocketed)
