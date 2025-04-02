import numpy as np
#representing a maze and solving it using floodfill 

#7*7 block maze
size = 7
maze = np.array([
    [6,5,4,3,4,5,6],
    [5,4,3,2,3,4,5],
    [4,3,2,1,2,3,4],
    [3,2,1,0,1,2,3],
    [4,3,2,1,2,3,4],
    [5,4,3,2,3,4,5],
    [6,5,4,3,4,5,6]
])

#enum for directional movement
class Direction:
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

start_pos = [0,0]
current_pos = start_pos

def walk(direction):
    move_x, move_y = direction_offsets[direction][:2]
    current_pos[0] += move_x
    current_pos[1] += move_y

def move_to_target(pos=[0, 0], finish_pos=[(size - 1) // 2, (size - 1) // 2]):
    distance = maze[pos[0], pos[1]]

    # Calculate values for all directions
    direction_values = {}
    for direction, (dx, dy, bit) in direction_offsets.items():
        try:
            direction_values[direction] = maze[pos[0] + dx, pos[1] + dy]
        except IndexError:
            direction_values[direction] = size  # Assign a large value for out-of-bounds

    if distance == 0 or pos == finish_pos:
        print("Maze solved!")
        exit()

    # Find the direction with the next lower value
    for direction, (dx, dy, bit) in direction_offsets.items():
        if direction_values[direction] == distance - 1:
            walk(direction)
            break
    print(current_pos)
    move_to_target(current_pos, finish_pos)
    
move_to_target()

#Here we will create an example maze and solve it
#use bitmask to encode walls in each direction
#TODO - add real maze walls
maze_to_solve = np.array([
    [0b1001, 0b0001, 0b0001, 0b0001, 0b0001, 0b0001, 0b0011],
    [0b1000, 0b0001, 0b0001, 0b0001, 0b0001, 0b0001, 0b0011],
    [0b1000, 0b0001, 0b0001, 0b0001, 0b0001, 0b0001, 0b0011],
    [0b1000, 0b0001, 0b0001, 0b0001, 0b0001, 0b0001, 0b0011],
    [0b1000, 0b0001, 0b0001, 0b0001, 0b0001, 0b0001, 0b0011],
    [0b1000, 0b0001, 0b0001, 0b0001, 0b0001, 0b0011, 0b0010],
    [0b1001, 0b0001, 0b0001, 0b0011, 0b0001, 0b0001, 0b0110],
])



