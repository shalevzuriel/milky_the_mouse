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

def move_to_target(pos=[0, 0], finish_pos=[(size - 1) // 2, (size - 1) // 2]):
    distance = maze[pos[0], pos[1]]
    directions = {
        Move.UP: (-1, 0),
        Move.RIGHT: (0, 1),
        Move.DOWN: (1, 0),
        Move.LEFT: (0, -1),
    }

    # Calculate values for all directions
    direction_values = {}
    for direction, (dx, dy) in directions.items():
        try:
            direction_values[direction] = maze[pos[0] + dx, pos[1] + dy]
        except IndexError:
            direction_values[direction] = size  # Assign a large value for out-of-bounds

    if distance == 0 or pos == finish_pos:
        print("Maze solved!")
        exit()

    # Find the direction with the next lower value
    for direction, (dx, dy) in directions.items():
        if direction_values[direction] == distance - 1:
            walk(direction)
            break

    print(current_pos)
    move_to_target(current_pos, finish_pos)
    
move_to_target()


