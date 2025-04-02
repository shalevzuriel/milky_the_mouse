import numpy as np
#representing a maze and solving it using floodfill 

#7*7 block maze
size = 7
maze = np.array([[6,5,4,3,4,5,6],
                [5,4,3,2,3,4,5],
                [4,3,2,1,2,3,4],
                [3,2,1,0,1,2,3],
                [4,3,2,1,2,3,4],
                [5,4,3,2,3,4,5],
                [6,5,4,3,4,5,6]])

#enum for directional movement
class Move:
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

start_pos = [0,0]
current_pos = start_pos

def walk(direction):
    if direction == Move.RIGHT:
        current_pos[1] += 1
    if direction == Move.LEFT:
        current_pos[1] -= 1
    if direction == Move.UP:
        current_pos[0] -= 1
    if direction == Move.DOWN:
        current_pos[0] += 1

def move_to_target(pos=[0,0], finish_pos=[(size - 1)/2, (size - 1)/2]):
    distance = maze[pos[0], pos[1]]
    #TODO - fix repetative code
    try:
        up_val = maze[pos[0] - 1, pos[1]]
    except:
        up_val = size #a big value for now
    try:
        right_val = maze[pos[0], pos[1] + 1]
    except:
        right_val = size
    try:
        down_val = maze[pos[0] + 1, pos[1]]
    except:
        down_val = size
    try:
        left_val = maze[pos[0], pos[1] - 1]
    except: 
        left_val = size
    
    if distance == 0 or pos == finish_pos: 
        print("Maze solved!")
        exit()
    elif up_val == distance - 1:
        walk(Move.UP)
    elif right_val == distance -1:
        walk(Move.RIGHT)
    elif down_val == distance -1:
        walk(Move.DOWN)
    elif left_val == distance - 1:
        walk(Move.LEFT)
    
    print(current_pos)
    move_to_target(current_pos, finish_pos)
    
move_to_target()


