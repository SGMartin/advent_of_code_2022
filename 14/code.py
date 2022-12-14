import numpy as np

## Functions definitions ##


def get_coords_from_string(rock):
    x, y = rock.split(",")

    return (int(x), int(y))


def get_cave_size(all_rocks):
    max_x, max_y = 0, 0
    for rock in all_rocks:
        if rock[0] > max_x:
            max_x = rock[0]
        if rock[1] > max_y:
            max_y = rock[1]

    return (max_x + 1, max_y + 1)


def is_out_of_bounds(position, this_cave, full=True):
    if full:
        if position[0] >= this_cave.shape[0] or position[1] >= this_cave.shape[1]:
            return True
        else:
            return False
    else:
        height_too_low = True if position[1] >= this_cave.shape[1] else False
        return height_too_low


def can_move(position, direction, this_cave, full=True):
    offset = 1 if direction == "right" else (-1 if direction == "left" else 0)
    coords = (position[0] + offset, position[1] + 1)
    if is_out_of_bounds(coords, this_cave, full=full):
        return False
    else:
        occupied = this_cave[coords[0], coords[1]]
        return not occupied


def move_sand(position, this_cave, full=True):
    if can_move(position, "down", this_cave, full=full):
        return (position[0], position[1] + 1)
    if can_move(position, "left", this_cave, full=full):
        return (position[0] - 1, position[1] + 1)
    if can_move(position, "right", this_cave, full=full):
        return (position[0] + 1, position[1] + 1)

    return False


def spawn_sand(this_cave):
    position = (500, 0)
    rested = False

    while not rested:
        if move_sand(position, this_cave, full=True):
            position = move_sand(position, this_cave, full=True)
        else:
            rested = True
            ## Check if we are unable to move or at the abyss
            if position[1] == this_cave.shape[1] - 1:
                return False
            else:
                break

    return position


def stack_sand(this_cave):
    position = (500, 0)
    rested = False

    while not rested:
        if move_sand(position, this_cave, full=True):
            position = move_sand(position, this_cave, full=True)
        else:
            rested = True
            break

    return position


def generate_cave(rock_paths, abyss=True):
    ## Flatten and transform everything to coords to get the max. cave size
    all_rock_paths = [
        get_coords_from_string(rock) for path in rock_paths for rock in path
    ]
    max_cave_size = get_cave_size(all_rock_paths)

    if not abyss:
        ## This is awful but I'm reeaaaally tired today
        max_cave_size = (max_cave_size[0] + 10000, max_cave_size[1])

    ## Initialize the cave according to the max. dims.
    cave = np.zeros(max_cave_size, dtype=bool)

    for path in rock_paths:
        for rock_id, rock in enumerate(path):
            if rock_id + 1 < len(path):
                this_coords = get_coords_from_string(rock)
                next_coords = get_coords_from_string(path[rock_id + 1])

                range_x = sorted([this_coords[0], next_coords[0]])
                range_y = sorted([this_coords[1], next_coords[1]])

                cave[range_x[0] : range_x[1] + 1, range_y[0] : range_y[1] + 1] = True

    ## Generate a ground floor at y + 2
    if not abyss:
        floor = np.ones((cave.shape[0], 1), dtype=bool)
        floor[
            :, 0
        ] = False  ## there is a gap between the floor and the last rock of a row)
        cave = np.hstack([cave, floor])

    return cave


with open("puzzle_input.txt", "r") as fil:
    lines = [line.rstrip() for line in fil.readlines()]

rock_paths = [line.split(" -> ") for line in lines]
part1_cave = generate_cave(rock_paths, abyss=True)

sand_stream = True
sand_count = 0

while sand_stream and sand_count < part1_cave.size:
    sand_rest_position = spawn_sand(part1_cave)
    # Sand spawn
    if sand_rest_position:
        sand_count += 1
        part1_cave[sand_rest_position[0], sand_rest_position[1]] = True
    else:
        sand_stream = False
        break


print(f"Part 1 answer is {sand_count}")

## Part #2, now there is no abyss
part2_cave = generate_cave(rock_paths, abyss=False)

hole_filled = False
sand_filled = 0

while not hole_filled and sand_filled < part2_cave.size:
    last_sand_position = stack_sand(part2_cave)
    is_at_start = all([(a == b) for a, b in zip(last_sand_position, (500, 0))])

    if last_sand_position and not is_at_start:
        sand_filled += 1
        part2_cave[last_sand_position[0], last_sand_position[1]] = True
    else:
        sand_filled += 1
        hole_filled = True
        break

print(f"Part 2 answer is {sand_filled}")
