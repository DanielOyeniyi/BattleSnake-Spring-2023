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
    my_head: dict = game_state['you']['body'][0]  # Coordinates of your head
    next_moves: list = make_directions(my_head)
    boundaries: list = make_boundaries(game_state) 
    snakes: list = make_snakes(game_state)
    food: dict = closest_food(game_state, my_head)
    food_moves: list = move_towards(my_head, food)
    
    safe_moves: list = []
    for move in next_moves:
        if move[1] not in boundaries and move[1] not in snakes:
            safe_moves.append(move[0])  

    tmp:list = []
    for move in next_moves:
        if move[0] in safe_moves and check_collisions(game_state, move[1]):
            tmp.append(move[0])

    if (len(tmp) != 0):        # avoids moves with high chance of collision
        safe_moves = tmp
      
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    optimal: list = []
    max: int = 0
    for move in next_moves:
        if move[0] in safe_moves:
            value: int = connected(game_state, move[1])
            optimal.append(((move[0]),value))
            if value > max:
                max = value

    max_connected: list = []
    for move in optimal:
        if move[1] >= max:
            max_connected.append(move[0])
            max = move[1]
          
    safe_moves = max_connected
    tmp = []
    for move in food_moves:
        if move in safe_moves:
            tmp.append(move)
          
    food_moves = tmp
  
    if len(food_moves) != 0:
        next_move = random.choice(food_moves)
        print(f"MOVE {game_state['turn']}: {next_move}")
        return {"move": next_move}
      
    else:     
        next_move: list  = random.choice(safe_moves)
        print(f"MOVE {game_state['turn']}: {next_move}")
        return {"move": next_move}
      
def make_directions(position: dict) -> list:
    '''
    calculates the right, left, up, and down positons from the given position
  
    param postion: a dict containing the coordinates of the given position
    return: a list of tuples containing the directions and thei coordinates
    '''
    right = {"x": position['x']+1, "y": position['y']}
    left = {"x": position['x']-1, "y": position['y']}
    up = {"x": position['x'], "y": position['y']+1}
    down = {"x": position['x'], "y": position['y']-1}
    return [("right", right), ("left", left), ("up", up), ("down", down)]
  
def make_boundaries(game_state: dict) -> list:
    '''
    calculates the boundaries of the board and stores them  in a list
  
    param game_state: a dict containing all the games information
    return:  a list containing dicts of coordinates
    '''
    boundaries: list = []
    board_width: int = game_state['board']['width']
    board_height: int = game_state['board']['height']
    
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
    snakes: list = []
    for snake in  game_state['board']['snakes']:
      for body in snake['body']:
          if body != snake['body'][-1]:        # tail
              snakes.append(body)
          elif include_tail(game_state, snake['body'][0]):
              snakes.append(body)
  
    return snakes
  
def check_collisions(game_state: dict, position: dict) -> bool:
    '''
    checks if the position has a chance of colliding with the head
    of a bigger snake
  
    param game_state: a dict containing all the games information
    param postion: a dict containing the coordinates of the given position
    return:  True if there is a chance of collision
    '''
    my_head: dict = game_state['you']['body'][0] 
    my_length: int = game_state['you']['length']
    directions: list = make_directions(position)
    snake_heads: list = []

    for snake in game_state['board']['snakes']:
        snake_head: dict = snake['body'][0]
        if snake['length'] >= my_length and snake_head != my_head:
            snake_heads.append(snake_head)

    for direction in directions:
        if direction[1] in snake_heads:
            return False
          
    return True

def include_tail(game_state: dict, head: dict) -> bool:
    '''
    checks if the snake has a chance of growing 
  
    param game_state: a dict containing all the games information
    param head: a dict containing the coordinates of the given snake head
    return:  True if there is a chance of the snake growing
    '''
    directions: list = make_directions(head)

    for direction in directions:
        if direction[1] in game_state['board']['food']:
            return True
      
    return False    

def closest_food(game_state: dict, position: dict) -> dict:
    '''
    returns the coordinates of the closest food on the board
  
    param game_state: a dict containing all the games information
    param postion: a dict containing the coordinates of the given position
    return:  a list containing dicts of coordinates
    '''
    min: dict = {"position": "", "distance": game_state["board"]["width"] + game_state["board"]["height"] }
    for food in game_state['board']['food']:
      distance: int = abs(food['x'] - position['x'])
      distance += abs(food['y'] - position['y'])
      if distance < min['distance']:
          min['position'] = food
          min['distance'] = distance
    return min['position']

def connected(game_state: dict, position) -> int:
    '''
    calculates the number of coordinates connected to the given position
  
    param game_state: a dict containing all the games information
    param postion: a dict containing the coordinates of the given position
    return: an int representing the number of coordinates
    '''
    board_width: int = game_state['board']['width']
    board_height: int = game_state['board']['height']
    marked: list = [[False]*board_width for i in range(board_height)]
    snakes = make_snakes(game_state)
    boundaries = make_boundaries(game_state)
    return connected_helper(snakes, boundaries, position, marked)

def connected_helper(snakes: dict, boundaries: dict, position: dict, marked: list) -> int:
    '''
    Helper for 'connected' fucntion
  
    param snakes: a dict containing all the snake coordinates on the board
    param boundaries: a dict containing all the boundary coordinates on the board
    param postion: a dict containing the coordinates of the given position
    param marked: a 2D list representing coordinates
    return: an int representing the number of coordinates
    '''
    if position in snakes or position in boundaries or marked[position['x']][position['y']]:
        return 0
      
    marked[position['x']][position['y']] = True
      
    directions = make_directions(position)
    return (1 + connected_helper(snakes, boundaries, directions[0][1], marked) 
              + connected_helper(snakes, boundaries, directions[1][1], marked) 
              + connected_helper(snakes, boundaries, directions[2][1], marked) 
              + connected_helper(snakes, boundaries, directions[3][1], marked))


def move_towards(position: dict, target: dict):
    '''
    returns the directions of the target relative to the position
  
    param postion: a dict containing the coordinates of the given position
    param target: a dict containing the coordinates of the target position
    return:  a list containing direction strings
    '''
    moves = []
    if position['x'] < target['x']:
        moves.append("right")
      
    if position['x'] > target['x']:
        moves.append("left")
      
    if position['y'] < target['y']:
        moves.append("up")
    if position['y'] > target['y']:
        moves.append("down")
    return moves
  
# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
