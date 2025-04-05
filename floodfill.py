import numpy as np
from enum import Enum
#representing a maze and solving it using floodfill 

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


def walk(cell, direction):
    move_x, move_y = direction_offsets[direction][:2]
    cell[0] += move_x
    cell[1] += move_y
    return cell

def has_wall(maze, pos, direction):
    _, _, mask = direction_offsets[direction]
    return maze[pos[0], pos[1]] & mask != 0

#This is the video about floodfill: https://youtu.be/ktn3C7aXVR0?si=hgcQJnGxJFgDgqat
def floodfill(maze_to_solve, start_cell, target_cell):
    size = len(maze_to_solve)
    maze_dis = np.full((size, size), np.nan)
    maze_dis[target_cell[0], target_cell[1]] = 0
    cell_queue = [target_cell]
    current_cell = cell_queue.pop(0)
    while current_cell != start_cell:
        distance = maze_dis[current_cell[0], current_cell[1]]
        for direction, (dx, dy, bit) in direction_offsets.items():
            neighbor_cell = [current_cell[0] + dx, current_cell[1] + dy]
            try: 
                if neighbor_cell[0] < 0 or neighbor_cell[1] < 0:
                    raise IndexError("Index out of bounds")
                neighbor_cell_dis = maze_dis[neighbor_cell[0], neighbor_cell[1]]
            except IndexError:
                continue
            if has_wall(maze_to_solve, current_cell, direction) or (not np.isnan(neighbor_cell_dis)):
                continue
            cell_queue.append(neighbor_cell)
            maze_dis[neighbor_cell[0], neighbor_cell[1]] = distance + 1
        current_cell = cell_queue.pop(0)
    print(maze_dis)
    return maze_dis


def move_to_target(maze_to_solve, maze_dis, start_cell, target_cell):
    current_cell = start_cell
    distance = maze_dis[current_cell[0], current_cell[1]]
    print(current_cell)
    if current_cell == target_cell:
        print("Maze solved!")
        return
    for direction, (dx, dy,_) in direction_offsets.items():
        neighbor_cell = [current_cell[0] + dx, current_cell[1] + dy]
        try: 
            if neighbor_cell[0] < 0 or neighbor_cell[1] < 0:
                raise IndexError("Index out of bounds")
            neighbor_cell_dis = maze_dis[neighbor_cell[0], neighbor_cell[1]]
        except IndexError:
            continue
        if (not has_wall(maze_to_solve, current_cell, direction)) and neighbor_cell_dis == distance - 1:
            current_cell = walk(current_cell, direction)
            break
    move_to_target(maze_to_solve,maze_dis, current_cell, target_cell)

def solve(maze_to_solve, start_cell, target_cell):
    maze_dis = floodfill(maze_to_solve, start_cell, target_cell)
    move_to_target(maze_to_solve, maze_dis, start_cell, target_cell)

#Here we will create an example maze and solve it
#use bitmask to encode walls in each direction
maze_example = np.array([
    [0b1001, 0b0001, 0b0011, 0b1011, 0b1001, 0b0011, 0b1011],
    [0b1010, 0b1010, 0b1100, 0b0110, 0b1010, 0b1010, 0b1010],
    [0b1010, 0b1010, 0b1001, 0b0011, 0b1010, 0b1100, 0b0110],
    [0b0110, 0b1010, 0b1100, 0b0100, 0b0100, 0b0001, 0b0011],
    [0b1001, 0b0110, 0b1001, 0b0001, 0b0011, 0b1110, 0b1010],
    [0b1010, 0b1001, 0b0110, 0b1010, 0b1000, 0b0011, 0b1010],
    [0b1100, 0b0110, 0b1001, 0b0110, 0b1110, 0b1100, 0b0110],
])

solve(maze_example, [3,0], [3,3])
#TODO - Method to update maze walls each cell and do floodfill each time
#1