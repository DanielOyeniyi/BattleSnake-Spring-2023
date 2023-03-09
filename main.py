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
        "color": "#ffe6e6",  # TODO: Choose color
        "head": "do-sammy",  # TODO: Choose head
        "tail": "cosmic-horror",  # TODO: Choose tail
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
    my_tail: dict = game_state['you']['body'][-1] 
    next_moves: list = make_directions(my_head)
    safe_moves: list = make_safe_moves(game_state)



    tail_access: list = []
    for move in next_moves:        # add moves that have a direct path to our tail
        if check_direct_path(game_state, move[1], my_tail):
            tail_access.append(move)

    tmp: list = []
    for move in tail_access:
        if move[0] in safe_moves:
            tmp.append(move[0])
    if len(tmp) != 0:
        safe_moves = tmp
  
    optimal: list = []         # choose the move that is connected to the greatest
    max: int = 0               # amount of space
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
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: {safe_moves}")
        return {"move": "down"}        

    destroy_moves = make_target_moves(game_state, safe_moves,"destroy") 
    destroy_moves = target_mid_point(game_state, destroy_moves)
              
    if len(destroy_moves) != 0:        # if here we are trying to kill another snake
        next_move: list  = random.choice(destroy_moves)
        print(f"MOVE {game_state['turn']}: {next_move}")
        return {"move": next_move}

    feast_moves: list = make_target_moves(game_state, safe_moves, "feast")
    feast_moves = target_mid_point(game_state, feast_moves)
      
    if len(feast_moves) != 0:          # if here we are tryin to chase food
        next_move: list  = random.choice(feast_moves)
        print(f"MOVE {game_state['turn']}: {next_move}")
        return {"move": next_move}

    safe_moves = target_mid_point(game_state, safe_moves)
    next_move: list  = random.choice(safe_moves)        # none of the previous options are possible to just 
    print(f"MOVE {game_state['turn']}: {next_move}")    # choose a direction that is connected to the most space
    return {"move": next_move}

def make_safe_moves(game_state: dict) -> list:
    '''
    returns a list of all the safe moves that avoid potential death
  
    param game_state: a dict containing all the games information
    return:  a list safe moves as strings
    '''
    next_moves: list = make_directions(game_state['you']['body'][0])
    boundaries: list = make_boundaries(game_state) 
    snakes: list = make_snakes(game_state)

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


    return safe_moves  

def make_target_moves(game_state: dict, safe_moves: list, mode: str) -> list:
    '''
    returns a list of all the safe moves towards a target, the target changes 
    depending on the mode. The target is either the closest smaller snake or
    the closest food to you where you are closer than any bigger snakes
  
    param game_state: a dict containing all the games information
    param safe_moves: a list of safe moves as strings
    return:  a list of moves towards the target
    '''
    my_head: dict = game_state['you']['body'][0]
    next_moves: list = make_directions(my_head)

    targets: list = []
    if mode == "destroy":
        targets = make_prey(game_state, safe_moves)
      
    if mode == "feast":
        targets = make_food(game_state, safe_moves)  
      
    target_moves: list = []
  
    for target in targets:
        possible: list = []
        if len(target_moves) == 0:
            for move in next_moves:
                if check_direct_path(game_state, move[1], target[0]) and move[0] in safe_moves:
                    possible.append(move)
            if len(possible) != 0:     
                tmp: list = move_towards(my_head, target[0])
                optimal: list = make_optimal(game_state, possible)
                if len(tmp) != 0:
                    for move in possible:
                        if move[0] in tmp and move[0] in optimal:
                            target_moves.append(move[0])
                      
    return target_moves 

def make_food(game_state: dict, safe_moves: list) -> list:
    '''
    returns a list of all the food that is safe to eat on the 
    board, the list is sorted by distance
  
    param game_state: a dict containing all the games information
    param safe_moves: a list of safe moves as strings
    return:  a list of tuples containg the food position and distance
    '''
    my_head: dict = game_state['you']['body'][0]
    my_length: int = game_state['you']['length']
    snake_heads: list = []
    food_list: list = []

    tmp: list = make_directions(my_head)
    next_moves: list = []
    for move in tmp:
        if move[0] in safe_moves:
            next_moves.append(move)
  
    for snake in game_state['board']['snakes']:
        if snake['length'] >= my_length and snake['body'][0] != my_head:
            snake_heads.append(snake['body'][0])
          
    for food in game_state['board']['food']:
        worth: bool = True
        my_distance: int = abs(food['x'] - my_head['x'])
        my_distance += abs(food['y'] - my_head['y'])
        for head in snake_heads:
            head_distance: int = abs(food['x'] - head['x'])
            head_distance += abs(food['y'] - head['y'])

            if my_distance >= head_distance:
                worth = False
     
        if worth: 
            direct_path: bool = False
            for move in next_moves:
                if check_direct_path(game_state, move[1], food):
                    direct_path = True

            if direct_path:
                food_list.append((food, my_distance))
          
    food_list = sorted(food_list, key=lambda tup: tup[1])
    return food_list

def make_prey(game_state: dict, safe_moves: dict) -> list:
    '''
    returns a list of all the smaller snake heads that is safe to 
    destroy on the board, the list is sorted by distance
  
    param game_state: a dict containing all the games information
    param safe_moves: a list of safe moves as strings
    return:  a list of tuples containing the snakeheads posiiton and distance
    '''
    my_head: dict = game_state['you']['body'][0]
    my_length: int = game_state['you']['length']
    prey: list = []

    tmp: list = make_directions(my_head)
    next_moves: list = []
    for move in tmp:
        if move[0] in safe_moves:
            next_moves.append(move)
  
    for snake in game_state['board']['snakes']:
        snake_head = snake['body'][0]
      
        if snake['length'] < my_length:
            direct_path: bool = False
            for move in next_moves:
                if check_direct_path(game_state, move[1], snake_head):
                    direct_path = True
            if direct_path:
                distance: int = abs(snake_head['x'] - my_head['x']) 
                distance += abs(snake_head['y'] - my_head['y'])
                prey.append((snake['body'][0], distance))
          
    prey = sorted(prey, key=lambda tup: tup[1])
    return prey

def make_optimal(game_state: dict, moves: list) -> list:
    '''
    finds the move that is connected the the greatest amount of the 
    board out of the given moves
  
    param game_state: a dict containing all the games information
    param moves: a list of moves that we want to find the optimal moves from
    return:  a list safe moves as strings
    '''
    connected_vals: list = []
    max: int = 0
    for move in moves:
        val: int = connected(game_state, move[1])
        connected_vals.append(((move[0]),val))
        if val > max:
            max = val

    optimal: list = []
    for move in connected_vals:
        if move[1] >= max:
            optimal.append(move[0])
            max = move[1]
    return optimal

def target_mid_point(game_state: dict, moves: list) -> list:
    my_head: dict = game_state['you']['body'][0]
    mid_point: dict = {'x':game_state['board']['width']//2,'y':game_state['board']['height']//2}
    tmp: list = move_towards(my_head, mid_point)
    
    new_moves: list = []
    for move in tmp: 
        if move in moves:
           new_moves.append(move)
    if len(new_moves) != 0:
        return new_moves
    return moves

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
          elif include_tail(game_state, snake):
              snakes.append(body)
  
    return snakes

def include_tail(game_state: dict, snake: dict) -> bool:
    '''
    checks if the snake has a chance of growing or just grew
  
    param game_state: a dict containing all the games information
    param head: a dict containing the information of the given snake
    return:  True if there is a chance of the snake growing or if the snake just grew
    '''
    if snake['length'] == 1:
        return False
      
    tail: dict = snake['body'][-1]
    before_tail = snake['body'][-2] 
    if tail == before_tail:   # snake just ate food
        return True
  
    head: dict = snake['body'][0]
    directions: list = make_directions(head)
    for direction in directions:
        if direction[1] in game_state['board']['food']:
            return True
      
    return False 
  
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

def check_direct_path(game_state: dict, position: dict, target: dict) -> bool:
    '''
    checks if there is a direct path from the postion to the target
  
    param game_state: a dict containing all the games information
    param postion: a dict containing the coordinates of the given position
    param target: a dict containing the coordinates of the given target
    return: True if there is a direct path
    '''
  
    board_width: int = game_state['board']['width']
    board_height: int = game_state['board']['height']
    marked: list = [[False]*board_width for i in range(board_height)]
    snakes = make_snakes(game_state)
    boundaries = make_boundaries(game_state)
  
    if check_direct_path_helper(snakes, boundaries, position, target, marked) > 0:
        return True
      
    return False

def check_direct_path_helper(snakes: list, boundaries: list, position: dict, target: dict, marked: list) -> int:
    '''
    Helper for 'check_direct_path'
  
    param snakes: a dict containing all the snake coordinates on the board
    param boundaries: a dict containing all the boundary coordinates on the board
    param postion: a dict containing the coordinates of the given position
    param target: a dict containing the coordinates of the given target
    param marked: a 2D list representing coordinates
    return: True if there is a direct path
    '''
    if (position == target):
        return 1
      
    if position in snakes or position in boundaries or marked[position['x']][position['y']]:
        return 0
      
    marked[position['x']][position['y']] = True
      
    directions = make_directions(position)
    return (0 + check_direct_path_helper(snakes, boundaries, directions[0][1], target, marked) 
              + check_direct_path_helper(snakes, boundaries, directions[1][1], target, marked) 
              + check_direct_path_helper(snakes, boundaries, directions[2][1], target, marked) 
              + check_direct_path_helper(snakes, boundaries, directions[3][1], target, marked))
    

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
    Helper for 'connected'
  
    param snakes: a dict containing all the snake coordinates on the board
    param boundaries: a dict containing all the boundary coordinates on the board
    param postion: a dict containing the coordinates of the given position
    param marked: a 2D list representing  coordinates
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
