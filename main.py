# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#f2c84e",  # TODO: Choose color
        "head": "sand-worm",  # TODO: Choose head
        "tail": "mlh-gene",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    next_moves = make_directions(my_head)
    boundaries = make_boundaries(game_state) 
    snakes = make_snakes(game_state)

    safe_moves = []
    for move in next_moves:
        if move[1] not in boundaries and move[1] not in snakes:
            safe_moves.append(move[0])  
      
      
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)
  
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

def make_directions(position: dict) -> list:
    '''
    calculates the right, left, up, and down positons from the given position
  
    param postion: a dict containing the coordinates of the given position
    return: a list of tuples containing the directions and thei coordinates
    '''
    right = {"x": position["x"]+1, "y": position["y"]}
    left = {"x": position["x"]-1, "y": position["y"]}
    up = {"x": position["x"], "y": position["y"]+1}
    down = {"x": position["x"], "y": position["y"]-1}
    return [("right", right), ("left", left), ("up", up), ("down", down)]
  
def make_boundaries(game_state: dict) -> list:
    '''
    calculates the boundaries of the board and stores them  in a list
  
    param game_state: a dict containing all the games information
    return:  a list containing dicts of coordinates
    '''
    boundaries = []
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    
    for  x  in  range(board_width):
      boundaries.append({"x": x, "y": -1})
      boundaries.append({"x": x, "y": board_height})
      
    for y  in  range(board_height):
      boundaries.append({"x": -1, "y": y})
      boundaries.append({"x": board_width, "y": y})
  
    return boundaries

def make_snakes(game_state: dict) -> list:
    '''
    stores the locations of all the snakes on the board in a list
  
    param game_state: a dict containing all the games information
    return:  a list containing dicts of coordinates
    '''
    snakes = []
    for snake in  game_state["board"]["snakes"]:
      for body in snake["body"]:
        snakes.append(body)
        
    for body in game_state["you"]["body"]:
      snakes.append(body)  
  
    return snakes
    
# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
