import numpy as np
from enum import Enum
#representing a maze and solving it using floodfill 

#7*7 block maze
size = 7
maze_dis = np.array([
    [6,5,4,3,4,5,6],
    [5,4,3,2,3,4,5],
    [4,3,2,1,2,3,4],
    [3,2,1,0,1,2,3],
    [4,3,2,1,2,3,4],
    [5,4,3,2,3,4,5],
    [6,5,4,3,4,5,6]
])

#enum for directional movement
class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

direction_offsets = {
    Direction.UP: (-1, 0, 0b0001),
    Direction.RIGHT: (0, 1, 0b0010),
    Direction.DOWN: (1, 0, 0b0100),
    Direction.LEFT: (0, -1, 0b1000),
}

start_pos = [3,0]
current_pos = start_pos

def walk(direction):
    move_x, move_y = direction_offsets[direction][:2]
    current_pos[0] += move_x
    current_pos[1] += move_y

position_history = [start_pos]

def move_to_target(maze_to_solve, pos=[0, 0], finish_pos=[(size - 1) // 2, (size - 1) // 2]):
    distance = maze_dis[pos[0], pos[1]]
    print(pos)
    if distance == 0 or pos == finish_pos:
        print("Maze solved!")
        return
    # Calculate values for all directions
    direction_values = {}
    for direction, (dx, dy,_) in direction_offsets.items():
        try:
            if pos[0] + dx < 0 or pos[1] + dy < 0:
                raise IndexError("Index out of bounds")
            direction_values[direction] = maze_dis[pos[0] + dx, pos[1] + dy]
        except IndexError:
            direction_values[direction] = size * size  # Assign a large value for out-of-bounds


    breaked = False
    lowest_dis = size * size
    for direction, (dx, dy,_) in direction_offsets.items():
        if has_wall(maze_to_solve, pos, direction):
            continue
        if direction_values[direction] == distance - 1:
            walk(direction)
            breaked = True
            break
        lowest_dis = min(lowest_dis, direction_values[direction])
    if breaked == False:
        update_maze_dis(maze_dis, position_history, lowest_dis - distance + 1)
    if pos != current_pos:
        position_history.append(current_pos)
    move_to_target(maze_to_solve, current_pos, finish_pos)
    

#Here we will create an example maze and solve it
#use bitmask to encode walls in each direction
#TODO - method that updated the maze distances with each step
#TODO - gradient decent with walls. 
maze_example = np.array([
    [0b1001, 0b0101, 0b0101, 0b0011, 0b1001, 0b0101, 0b0111],
    [0b1100, 0b0011, 0b1101, 0b0110, 0b1010, 0b1001, 0b0011],
    [0b1001, 0b0010, 0b1001, 0b0011, 0b1100, 0b0110, 0b1010],
    [0b0110, 0b1010, 0b1100, 0b0100, 0b0001, 0b0101, 0b0110],
    [0b1001, 0b0100, 0b0101, 0b0111, 0b1100, 0b0011, 0b1011],
    [0b1010, 0b1001, 0b0101, 0b0101, 0b0101, 0b0110, 0b1010],
    [0b1100, 0b0100, 0b1001, 0b0101, 0b0101, 0b0101, 0b0110],
])

def has_wall(maze, pos, direction):
    _, _, mask = direction_offsets[direction]
    return maze[pos[0], pos[1]] & mask != 0


def update_maze_dis(maze, pos_history, additional_dis):
    for i in range(len(pos_history)):
        place = pos_history[len(pos_history) - 1 - i]
        maze[place[0], place[1]] += additional_dis + i


move_to_target(maze_example, (3,0))
#print(len(position_history))

