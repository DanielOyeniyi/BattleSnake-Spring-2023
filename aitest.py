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
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
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

  '''
  I want to attempt a minmax algorithm for choosing the next move
  first with 1 call then we see if we can do it recursivly 
  then try the alpha/beta pruning. but it takes time to understand and I 
  %100 won't figure it out by saturday. 
  '''

  
    return {"move": "right"}

def minimax(snake, max_turn):
    '''
    I'm thinking return 1 if still alive, -1 if dead
    so check next move, worst case we have 4 moves at the start of the game
    after round 1 we only ever have 3 moves but we want to avoid 3^n calculations

    so we turn in direction that gives us the best odds for suvival 
    enemy snake (just 1 other snake for now) will pick the option that maximizes 
    their odds for survival. so we want to maximize our odds and minimize opponents odds

    however turns  are taken at the same time so the scores of other snakes would 
    be negative as their survival odds have a negative relationship with our survival odds?
    but that's not %100 true. 

    so we run the same algorithm for each snake but just flip the signs to go from
    maximizing to minimizing

    so the possible moves would have the same safe moves function for this
    at least the instant death components

    make snake objects, it might be a lot easier to code this way
    '''
    if  state = 0:  # 
        return 1  if  max_turn else return -1 

    moves = ["right", "left", "up", "down"]
    scores = []
    for move in moves:
        score = min_max(move)
    return max(scores)

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})